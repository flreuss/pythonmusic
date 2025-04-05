import wave
from collections.abc import Iterable
from copy import copy
from os.path import abspath
from threading import Lock
from typing import Mapping, Optional, Self

import numpy as np
import pyaudio

from pythonmusic.play.target import Target
from pythonmusic.util import key_to_frequency

__all__ = ["AudioSamplerTarget"]

I16_MAX: int = 32_767
I16_MIN: int = -32_768


class WaveSample:
    def __init__(self, path: str, amp: float, falloff: float, target_samplerate: int):
        self._path = path
        self._sample_rate: int
        self._data: bytes
        self._total_frames: int
        self._falloff = falloff

        with wave.open(abspath(path), "rb") as wav:
            self._sample_rate = wav.getframerate()
            self._total_frames = wav.getnframes()

            # FIXME: calculate this
            # CONTINUE: needs to resample
            print(self._sample_rate)
            assert self._sample_rate == target_samplerate

            raw_data = np.clip(
                np.frombuffer(wav.readframes(self._total_frames), dtype=np.int16) * amp,
                I16_MIN,
                I16_MAX,
            ).astype(np.int16)

            if wav.getnchannels == 1:
                data = np.repeat(raw_data[:, np.newaxis], 2, axis=1)
            else:
                data = raw_data.reshape(-1, wav.getnchannels())[:, :2]

            self._data = data.tobytes()

    def __len__(self) -> int:
        return len(self._data)

    def falloff_i(self, sample_rate: int) -> int:
        return round(self._falloff * float(sample_rate))

    def pitch(self, base_freq: float, target_freq: float) -> Self:
        new_sample = copy(self)

        # FIXME: do some pitching with numpy
        # i guess we just change the sample rate

        return new_sample

    def path(self) -> str:
        return self._path

    def sample_rate(self) -> int:
        return self._sample_rate

    def data(self) -> bytes:
        return self._data

    def falloff(self) -> float:
        return self._falloff


class Voice:
    def __init__(self, data: memoryview, velocity: float, falloff: int):
        self.data = data
        self.len = len(data)
        self.index = 0
        self.velocity = velocity
        self.falloff = falloff
        self.current_falloff: Optional[int] = None

    def __len__(self) -> int:
        return len(self.data)

    def chunk(self, size: int) -> Optional[memoryview]:
        if self.index >= self.len:
            return None

        start = self.index
        end = min(start + size, self.len)
        self.index += size

        return self.data[start:end]

    def do_falloff(self):
        self.current_falloff = min(self.len - self.index, self.falloff)


class AudioSamplerTarget(Target):
    def __init__(
        self,
        round_robin: bool = True,
        buffer_size: int = 512,
        sample_rate: int = 44_100,
        format: int = pyaudio.paInt16,
    ):
        """
        TODO

        Args:
            round_robin(bool): If `True`, causes the sampler to overlay new
                sounds over already playing notes on the same key. If multiple
                samples are provided for the same key, the sampler attempts to
                use different samples at the same time to avoid audio defects.
                If set to `False`, the sampler will instead stop already playing
                notes and then start the new sound.
            buffer_size(int): The size of each audio buffer. If you hear popping
                noises, try to increase this value.
            sample_rate(int): The sample rate of the imported wav files.
            format(int): Audio format as an int type. Defaults to 16-Bit audio,
                which is common.

        """
        super().__init__()

        self._round_robin = round_robin
        self._sample_rate = sample_rate
        self._buffer_size = buffer_size
        self._format = format

        self._samples: list[list[WaveSample]] = [[]] * 128
        self._voices: list[list[Voice]] = [[]] * 128

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

    def round_robin(self) -> bool:
        return self._round_robin

    def sample_rate(self) -> int:
        return self._sample_rate

    def buffer_size(self) -> int:
        return self._buffer_size

    def format(self) -> int:
        return self._format

    def _add_sample(self, key: int, sample: WaveSample):
        self._samples[key].append(sample)

    def remove_sample(self, key: int, path: str):
        try:
            # generator, uhhh
            _ = next(sample for sample in self._samples[key] if sample.path() == path)
        except StopIteration:
            raise ValueError('No sample found for "{path}"')

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
        map(
            lambda target_key: self._add_sample(
                target_key,
                (
                    sample.pitch(
                        key_to_frequency(base_key), key_to_frequency(target_key)
                    )
                    if pitch
                    else sample
                ),
            ),
            add_to,
        )

        # TODO: pitch

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
        del time_info
        del status
        del in_data

        return self._make_buffer(frame_count)

    def _has_sample_for_key(self, key: int) -> bool:
        return len(self._samples[key]) != 0

    def _new_voice(self, key: int, velocity: int):
        if not self._has_sample_for_key(key):
            return

        sample: WaveSample
        if self._round_robin:
            voices = len(self._voices[key])
            print(voices & len(self._samples))
            sample = self._samples[key][voices % len(self._samples)]
        else:
            sample = self._samples[key][0]

        self._voices[key].append(
            Voice(
                memoryview(sample.data()),
                velocity / 127,
                sample.falloff_i(self._sample_rate),
            )
        )

    def _stop_voice(self, key: int):
        voices = self._voices[key]
        if len(voices) > 0:
            voices[-1].do_falloff()

    def _remove_voice(self, key: int, index: int):
        del self._voices[key][index]

    def _make_buffer(self, frame_count: int) -> tuple[bytes, int]:
        # 32 bit should prevent overflow
        buffer = np.zeros((frame_count, 2), dtype=np.int32)

        with self._lock:
            for key_index, key in enumerate(self._voices):
                for voice_index, voice in enumerate(key):
                    chunk = voice.chunk(frame_count)
                    if not chunk:
                        self._remove_voice(key_index, voice_index)
                        continue

                    # data = np.array(chunk, dtype=np.int16)
                    data = np.frombuffer(chunk, dtype=np.int16).reshape(-1, 2)

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
