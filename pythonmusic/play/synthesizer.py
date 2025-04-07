import math
from abc import ABC, abstractmethod
from threading import Lock
from typing import Callable, Iterable, Mapping, Optional

import numpy as np
import pyaudio as pa
from numpy.typing import NDArray

from pythonmusic.constants import (
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
)
from pythonmusic.play.audio_stream import AudioStream
from pythonmusic.play.target import Target
from pythonmusic.util import clip, key_to_frequency

__all__ = ["Oscillator", "SineOscillator", "SynthesizerTarget"]

#
# def SineOscillator(t: float, frequency: float, amplitude: float, phase: float) -> float:
#     return math.sin(t + phase) * amplitude * 0.5
#
#
# def SquareOscillator(
#     t: float, frequency: float, amplitude: float, phase: float
# ) -> float:
#     return (
#         math.copysign(1.0, SineOscillator(t, frequency, 1.0, phase)) * amplitude * 0.5
# )


class OscillatorEffect(ABC):
    pass


class Oscillator(ABC):
    def __init__(self):
        self._effects = []

    @abstractmethod
    def sample(self, t: float, phase: float, amplitude: float) -> float: ...


class SineOscillator(Oscillator):
    def __init__(self):
        super().__init__()

    def sample(self, t: float, phase: float, amplitude: float) -> float:
        return math.sin(t + phase) * amplitude


class KeyItem:
    __slots__ = ("t", "step", "amp", "is_playing")

    def __init__(self, sample_rate: int, key: int, amp: float):
        self.t = 0.0
        self.step = (
            math.tau * key_to_frequency(key) / float(sample_rate)
        )  # tau = 2 * pi
        self.amp = amp
        self.is_playing = False


class SynthesizerTarget(AudioStream, Target):
    def __init__(
        self,
        oscillators: list[Oscillator] = [],
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        super().__init__(1, sample_rate, buffer_size, pa.paFloat32)

        self._oscillators = oscillators
        self._keys: list[KeyItem] = list(
            map(
                lambda key: KeyItem(sample_rate, key, 0.0),
                range(128),
            )
        )

    def note_on(self, channel: int, key: int, velocity: int):
        super().note_on(channel, key, velocity)
        item = self._keys[key]
        item.is_playing = True
        item.amp = float(velocity) * 0.007874015748031496 * 0.3  # 1/127

    def note_off(self, channel: int, key: int, velocity: int):
        super().note_off(channel, key, velocity)
        self._keys[key].is_playing = False
        # CONTINUE: need falloff effect or similar

    def stream_callback(
        self,
        in_data: Optional[bytes],
        frame_count: int,
        time_info: Mapping[str, float],
        status: int,
    ) -> tuple[bytes, int]:
        del time_info
        del status
        del in_data

        buffer = np.zeros(frame_count, dtype=np.float32)

        if not self._oscillators:
            return (buffer.tobytes(), pa.paContinue)

        with self._lock:
            for key, item in enumerate(self._keys):
                if not item.is_playing:
                    continue

                # TODO: phrase
                # TODO: maybe pool
                buffer += self._make_buffer_for_key(frame_count, key, 0.0)

        return (np.clip(buffer, -1.0, 1.0).tobytes(), pa.paContinue)

    def _make_buffer_for_key(
        self, buffer_size: int, key: int, phase: float
    ) -> NDArray[np.float32]:
        # we have at least one oscillator
        buffer = np.ones(buffer_size, dtype=np.float32)
        item = self._keys[key]

        for oscillator in self._oscillators:
            data = np.zeros(buffer_size, dtype=np.float32)
            for i in range(buffer_size):
                data[i] = oscillator.sample(item.t, phase, item.amp)
                item.t += item.step

            buffer *= data

        return buffer
