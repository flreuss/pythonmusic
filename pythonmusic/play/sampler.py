from collections.abc import Iterable
from copy import copy
from os.path import abspath
from threading import Lock
from typing import Mapping, Optional, Self, cast

import numpy as np
import pyaudio
from numpy.typing import NDArray

from pythonmusic.play.target import Target
from pythonmusic.util import key_to_frequency

__all__ = ["SamplerTarget"]

I16_MAX: int = 32_767
I16_MIN: int = -32_768


def falloff_f_to_i(falloff: float, sample_rate: int) -> int:
    return round(falloff * float(sample_rate))


class WaveSample:
    def __init__(self, path: str, amp: float, falloff: float, target_sample_rate: int):
        self.data: NDArray
        self.falloff = falloff

        base_sample_rate: int
        raw_data: NDArray
        base_sample_rate, raw_data = wavfile.read(abspath(path))

        sample_count, channels = cast(tuple[int, int], raw_data.shape)

        # make stereo
        if channels == 1:
            raw_data = np.repeat(raw_data[:, np.newaxis], 2, axis=1)
        else:
            raw_data = raw_data.reshape(-1, channels)[:, :2]

        # resample, if needed
        raw_data = (
            # resample(raw_data, sample_count, sample_rate, target_samplerate)
            cast(
                NDArray,
                signal.resample(
                    raw_data,
                    round(
                        float(sample_count * target_sample_rate)
                        / float(base_sample_rate)
                    ),
                ),
            )
            if base_sample_rate != target_sample_rate
            else raw_data
        )

        raw_data = np.clip(raw_data * amp, I16_MIN, I16_MAX).astype(np.int16)
        self.data = raw_data

    def __len__(self) -> int:
        return len(self.data)

    def clone(self) -> Self:
        new = copy(self)
        new.data = np.copy(self.data)
        return new


class Voice:
    def __init__(self, data: memoryview, velocity: float, falloff: int):
        self.data = data
        self.velocity = velocity
        self.index = 0
        self.falloff_frames = falloff
        self.remaining_falloff: Optional[int] = None

    def chunk(self, size: int) -> Optional[tuple[float, memoryview]]:
        if self.index >= len(self.data):
            return None

        start = self.index
        end = min(start + size, len(self.data))
        self.index += size

        multiplyer = self.velocity

        if self.remaining_falloff:
            multiplyer *= float(self.remaining_falloff) / float(self.falloff_frames)
            self.remaining_falloff = max(0, self.remaining_falloff - size)

            if self.remaining_falloff == 0:
                # end sample
                self.index = len(self.data)

        return multiplyer, self.data[start:end]

    def init_falloff(self):
        self.remaining_falloff = min(len(self.data) - self.index, self.falloff_frames)


class SamplerTarget(Target):
    def __init__(
        self,
        buffer_size: int = 512,
        sample_rate: int = 44_100,
        format: int = pyaudio.paInt16,
    ):
        """
        TODO

        Args:
            buffer_size(int): The size of each audio buffer. If you hear popping
                noises, try to increase this value.
            sample_rate(int): The sample rate of the imported wav files.
            format(int): Audio format as an int type. Defaults to 16-Bit audio,
                which is common.

        """
        super().__init__()

        self._sample_rate = sample_rate
        self._buffer_size = buffer_size
        self._format = format

        self._samples: list[Optional[WaveSample]] = [None] * 128
        self._voices: list[Optional[Voice]] = [None] * 128

        self._lock = Lock()
        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format=self._format,
            channels=2,
            rate=self._sample_rate,
            output=True,
            frames_per_buffer=self._buffer_size,
            stream_callback=self._callback,
        )

    def __del__(self):
        # just to be save, define the order
        # 1 end stream
        self._stream.stop_stream()
        self._stream.close()
        del self._stream

        # 2 remove lock
        del self._lock

        # 3 terminate pa
        self._pa.terminate()

    def sample_rate(self) -> int:
        return self._sample_rate

    def buffer_size(self) -> int:
        return self._buffer_size

    def format(self) -> int:
        return self._format

    def _add_sample(self, key: int, sample: WaveSample):
        self._samples[key] = sample

    def remove_sample(self, key: int):
        self._samples[key] = None

    def add_sample(
        self, path: str, key: int, base_amp: float = 1.0, falloff: float = 0.1
    ):
        self._add_sample(key, WaveSample(path, base_amp, falloff, self._sample_rate))

    def add_sample_for_keys(
        self,
        path: str,
        base_key: int,
        add_to: Iterable[int],
        pitch: bool = True,
        base_amp: float = 1.0,
        falloff: float = 0.1,
    ):
        sample = WaveSample(path, base_amp, falloff, self._sample_rate)

        if pitch:
            base_sample_rate = key_to_frequency(base_key)
            for target_key, target_sample in map(
                lambda key: (key, sample.clone()), add_to
            ):
                target_sample_rate = key_to_frequency(target_key)

                print(target_key, len(target_sample.data))

                sample.data = cast(
                    NDArray,
                    signal.resample(
                        sample.data,
                        round(
                            float(len(sample.data) * target_sample_rate)
                            / float(base_sample_rate)
                        ),
                    ),
                ).astype(np.int16)

                self._add_sample(target_key, target_sample)

        else:
            for target_key in add_to:
                self._add_sample(target_key, target_sample)

    def note_on(self, channel: int, key: int, velocity: int):
        super().note_on(channel, key, velocity)
        self._new_voice(key, velocity)

    def note_off(self, channel: int, key: int, velocity: int):
        super().note_off(channel, key, velocity)
        self._stop_voice(key)

    # IMPL
    def _callback(
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
        buffer = np.zeros((frame_count, 2), dtype=np.int32)

        with self._lock:
            for key_index, voice in enumerate(self._voices):
                if not voice:
                    continue

                chunk_info = voice.chunk(frame_count)
                if not chunk_info:
                    self._remove_voice(key_index)
                    continue

                multiplyer, chunk = chunk_info

                # data = np.array(chunk, dtype=np.int16)
                data = (
                    np.frombuffer(chunk, dtype=np.int16)
                    .reshape(-1, 2)
                    .astype(np.float32)
                )
                data *= multiplyer
                data = np.clip(np.round(data), I16_MIN, I16_MAX).astype(np.int16)

                # if sample has run out, add padding
                data_len = len(data)
                if data_len < frame_count:
                    padding = np.zeros((frame_count - data_len, 2), dtype=np.int16)
                    data = np.vstack((data, padding))

                buffer += data.astype(np.int32)

        # clip back to 16 bits
        return (
            np.clip(buffer, I16_MIN, I16_MAX).astype(np.int16).tobytes(),
            pyaudio.paContinue,
        )

    def _new_voice(self, key: int, velocity: int):
        if self._samples[key] is None:
            return

        sample = self._samples[key]

        if sample:
            self._voices[key] = Voice(
                memoryview(sample.data),
                velocity / 127,
                falloff_f_to_i(sample.falloff, self._sample_rate),
            )

    def _stop_voice(self, key: int):
        voice = self._voices[key]
        if voice:
            voice.init_falloff()

    def _remove_voice(self, key: int):
        self._voices[key] = None
