from collections.abc import Iterable
from copy import copy
from os.path import abspath
from threading import Lock
from typing import Mapping, Optional, Self

import librosa as lr
import numpy as np
import pyaudio as pa
from numpy.typing import NDArray

from pythonmusic.play.audio_steam import AudioStream
from pythonmusic.play.target import Target

__all__ = ["SamplerTarget"]

I16_MAX: int = 32_767
I16_MIN: int = -32_768


def falloff_f_to_i(falloff: float, sample_rate: int) -> int:
    return round(falloff * float(sample_rate))


class WaveSample:
    def __init__(self, samples: NDArray, falloff: float):
        self.data = samples
        self.falloff = falloff

    @classmethod
    def load(cls, path: str, amp: float, falloff: float, target_sample_rate: int):

        raw_data: NDArray
        raw_data, _ = lr.load(abspath(path), sr=target_sample_rate, mono=False)

        if raw_data.ndim == 1:
            raw_data = np.vstack([raw_data, raw_data])  # mono → fake stereo
        elif raw_data.shape[0] > 2:
            raw_data = raw_data[:2, :]  # drop channels beyond stereo

        raw_data = np.clip(raw_data * amp, I16_MIN, I16_MAX).astype(np.float32)

        return cls(raw_data.T, falloff)

    def __len__(self) -> int:
        return len(self.data)

    def clone(self) -> Self:
        new = copy(self)
        new.data = np.copy(self.data)
        return new

    def pitch(self, semitones: int, sample_rate: int):
        self.data = lr.effects.pitch_shift(
            self.data.T, sr=sample_rate, n_steps=semitones, res_type="soxr_qq"
        ).T


class Voice:
    def __init__(self, data: NDArray, velocity: float, falloff: int):
        self.data = data
        self.velocity = velocity
        self.index = 0
        self.falloff_frames = falloff
        self.remaining_falloff: Optional[int] = None

    def chunk(self, size: int) -> Optional[NDArray]:
        if self.index >= len(self.data):
            return None

        start = self.index
        end = min(start + size, len(self.data))
        self.index += size

        multiplier = self.velocity

        if self.remaining_falloff:
            multiplier *= float(self.remaining_falloff) / float(self.falloff_frames)
            self.remaining_falloff = max(0, self.remaining_falloff - size)

            if self.remaining_falloff == 0:
                # end sample
                self.index = len(self.data)

        return self.data[start:end] * multiplier

    def init_falloff(self):
        self.remaining_falloff = min(len(self.data) - self.index, self.falloff_frames)


class SamplerTarget(AudioStream, Target):
    def __init__(
        self,
        sample_rate: int = 44_100,
        buffer_size: int = 512,
    ):
        """
        TODO

        Args:
            sample_rate(int): The sample rate of the imported wav files.
            buffer_size(int): The size of each audio buffer. If you hear popping
                noises, try to increase this value.
        """
        super().__init__(2, sample_rate, buffer_size, pa.paFloat32)

        self._samples: list[Optional[WaveSample]] = [None] * 128
        self._voices: list[Optional[Voice]] = [None] * 128

    def sample_count(self) -> int:
        """
        Returns the total number of loaded samples.
        """
        return len(list(filter(lambda element: element is not None, self._samples)))

    def voices(self) -> int:
        """
        Returns the number of active voices.
        """
        return len(self._voices)

    def _add_sample(self, key: int, sample: WaveSample):
        self._samples[key] = sample

    def remove_sample(self, key: int):
        self._samples[key] = None

    def add_sample(
        self, path: str, key: int, base_amp: float = 1.0, falloff: float = 0.1
    ):
        self._add_sample(
            key, WaveSample.load(path, base_amp, falloff, self._sample_rate)
        )

    def add_sample_for_keys(
        self,
        path: str,
        base_key: int,
        add_to: Iterable[int],
        pitch: bool = True,
        base_amp: float = 1.0,
        falloff: float = 0.1,
    ):
        sample = WaveSample.load(path, base_amp, falloff, self._sample_rate)

        if pitch:
            key_count = len(list(add_to))
            for index, target_key in enumerate(add_to):
                print(
                    f"pitching samples ({index + 1}/{key_count})", end="\r", flush=True
                )

                new_sample = sample.clone()
                if target_key != base_key:
                    new_sample.pitch(target_key - base_key, self._sample_rate)

                self._add_sample(target_key, new_sample)
            print()
        else:
            for target_key in add_to:
                self._add_sample(target_key, sample)

    def note_on(self, channel: int, key: int, velocity: int):
        super().note_on(channel, key, velocity)
        self._new_voice(key, velocity)

    def note_off(self, channel: int, key: int, velocity: int):
        super().note_off(channel, key, velocity)
        self._stop_voice(key)

    # IMPL
    def stream_callback(
        self,
        in_data: Optional[bytes],
        frame_count: int,
        time_info: Mapping[str, float],
        status: int,
    ) -> tuple[bytes, int]:
        # unused parameters
        del time_info
        del status
        del in_data

        # 32 bit should prevent overflow
        buffer = np.zeros((frame_count, 2), dtype=np.float32)

        with self._lock:
            for key_index, voice in enumerate(self._voices):
                if not voice:
                    continue

                data = voice.chunk(frame_count)
                if data is None:
                    self._remove_voice(key_index)
                    continue

                # if sample has run out, add padding
                data_len = len(data)
                if data_len < frame_count:
                    padding = np.zeros((frame_count - data_len, 2), dtype=np.float32)
                    data = np.vstack((data, padding))

                buffer += data.astype(np.float32)

        return (
            np.clip(buffer, -1.0, 1.0).tobytes(),
            pa.paContinue,
        )

    def _new_voice(self, key: int, velocity: int):
        if self._samples[key] is None:
            return

        sample = self._samples[key]

        if sample:
            self._voices[key] = Voice(
                sample.data,
                velocity / 127,
                falloff_f_to_i(sample.falloff, self._sample_rate),
            )

    def _stop_voice(self, key: int):
        voice = self._voices[key]
        if voice:
            voice.init_falloff()

    def _remove_voice(self, key: int):
        self._voices[key] = None
