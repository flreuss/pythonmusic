import math
from abc import ABC, abstractmethod
from typing import Mapping, Optional, cast, override

import numpy as np
import pyaudio as pa
from numpy.typing import NDArray

from pythonmusic.constants import (
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
)
from pythonmusic.play.audio_stream import AudioStream
from pythonmusic.play.target import Target
from pythonmusic.util import key_to_frequency, samples_to_seconds, seconds_to_samples

__all__ = [
    "Oscillator",
    "SineOscillator",
    "SquareOscillator",
    "SawOscillator",
    "SynthesizerTarget",
]

ONE_OVER_128: float = 0.0078125
BASE_AMP: float = 0.333
TAU: float = np.pi * 2


class _SynthKeyItem:
    __slots__ = ("t", "step", "amp", "duration", "attack", "sustain", "decay")

    def __init__(self, step: float):
        self.t = 0.0
        self.step = step
        self.amp = 1.0
        self.duration: Optional[int] = None
        self.attack: Optional[int] = None
        self.sustain: Optional[int] = None
        self.decay: Optional[int] = None

    def is_alive(self) -> bool:
        return self.duration is not None

    def begin(self):
        self.duration = 0

    def queue_end(self):
        self.duration = 0
        self.attack = None
        self.sustain = None
        self.decay = 100

    def end(self):
        self.duration = None


class Oscillator(ABC):
    """
    A base class for oscillators.

    To create a class from this, implement the
    :meth:`sample() <pythonmusic.play.Oscillator.sample>`
    method.

    Oscillators should not store and timing data internally, but rely on the
    passed ``t`` parameter in the
    :meth:`sample() <pythonmusic.play.Oscillator.sample>` function.
    """

    def _make_buffer_for_key(
        self, buffer_size: int, t: float, step: float, phase: float, amp: float
    ) -> NDArray[np.float32]:
        buffer = np.zeros(buffer_size, dtype=np.float32)

        for i in range(buffer_size):
            buffer[i] = self.sample(t, phase, amp)
            t += step

        return buffer

    @abstractmethod
    def sample(self, t: float, phase: float, amplitude: float) -> float:
        """
        This method is used to generate samples from the oscillator.

        Args:
            t (float): Timing offset for the oscillator. Used by the synthesizer
                to implement pitch
            phase (float): Timing offset (phase)
            amplitude (float): Amplitude multiplier (volume)
        """


class SineOscillator(Oscillator):
    """
    A sine oscillator.
    """

    def __init__(self):
        pass

    @override
    def _make_buffer_for_key(
        self, buffer_size: int, t: float, step: float, phase: float, amp: float
    ) -> NDArray[np.float32]:
        return np.sin(phase + t + (step * np.arange(buffer_size))) * amp

    def sample(self, t: float, phase: float, amplitude: float) -> float:
        # SineOscillator overwrites _make_buffer_for_key, to create the sine
        # with pure numpy. The below formular could be used instead.
        # (unused)
        return math.sin(t + phase) * amplitude


class SquareOscillator(SineOscillator):
    """
    A square oscillator.
    """

    def __init__(self):
        super().__init__()

    @override
    def sample(self, t: float, phase: float, amplitude: float) -> float:
        return (1.0 if super().sample(t, phase, 1.0) > 0.5 else 0.0) * amplitude

    @override
    def _make_buffer_for_key(
        self, buffer_size: int, t: float, step: float, phase: float, amp: float
    ) -> NDArray[np.float32]:
        return (
            np.where(
                super()._make_buffer_for_key(buffer_size, t, step, phase, 1.0) > 0.5,
                1.0,
                0.0,
            )
            * amp
        )


class SawOscillator(Oscillator):
    """
    A saw oscillator.
    """

    def __init__(self):
        pass

    @override
    def sample(self, t: float, phase: float, amplitude: float) -> float:
        return ((t + phase) % 1.0) * amplitude

    @override
    def _make_buffer_for_key(
        self, buffer_size: int, t: float, step: float, phase: float, amp: float
    ) -> NDArray[np.float32]:
        return (phase + t + step * np.arange(buffer_size)) % TAU * amp


class SynthesizerTarget(AudioStream, Target):
    """
    A synthesizer that uses :obj:`oscillators <pythonmusic.play.Oscillator>` for
    sound data generation.

    This target supports attack, sustain, and decay, which can be used to
    customise the oscillator's sound.

    Args:
        oscillator (Oscillator): An oscillator
        attack (Optional[float]): Attack in seconds
        sustain (Optional[float]): Sustain in seconds
        decay (Optional[float]): Decay in seconds
        sample_rate(int): Sample rate per second
        buffer_size(int): Sample buffer size
    """

    def __init__(
        self,
        oscillator: Oscillator,
        attack: Optional[float] = None,
        sustain: Optional[float] = None,
        decay: Optional[float] = None,
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        super().__init__(1, sample_rate, buffer_size, pa.paFloat32)
        self._sample_rate = sample_rate
        self._buffer_size = buffer_size
        self._keys = list(
            map(
                lambda key: _SynthKeyItem(
                    math.tau * key_to_frequency(key) / float(sample_rate)
                ),
                range(128),
            )
        )

        self._oscillator = oscillator
        self._attack = seconds_to_samples(attack, sample_rate) if attack else None
        self._sustain = seconds_to_samples(sustain, sample_rate) if sustain else None
        self._decay = seconds_to_samples(decay, sample_rate) if decay else None

    @property
    def oscillator(self) -> Oscillator:
        return self._oscillator

    @oscillator.setter
    def oscillator(self, v: Oscillator):
        self._oscillator = v

    @property
    def attack(self) -> Optional[float]:
        return (
            samples_to_seconds(self._attack, self._sample_rate)
            if self._attack
            else None
        )

    @attack.setter
    def attack(self, v: Optional[float]):
        self._attack = seconds_to_samples(v, self._sample_rate) if v else None

    @property
    def sustain(self) -> Optional[float]:
        return (
            samples_to_seconds(self._sustain, self._sample_rate)
            if self._sustain
            else None
        )

    @sustain.setter
    def sustain(self, v: Optional[float]):
        self._sustain = seconds_to_samples(v, self._sample_rate) if v else None

    @property
    def decay(self) -> Optional[float]:
        return (
            samples_to_seconds(self._decay, self._sample_rate) if self._decay else None
        )

    @decay.setter
    def decay(self, v: Optional[float]):
        self._decay = seconds_to_samples(v, self._sample_rate) if v else None

    def sample_rate(self) -> int:
        """Returns the synth's sample rate."""
        return self._sample_rate

    def buffer_size(self) -> int:
        """Returns the synth's buffer size."""
        return self._buffer_size

    def is_playing(self, key: int) -> bool:
        """Returns `True` if a note for the given key is playing."""
        return self._keys[key].is_alive()

    def _get_item_for_key(self, key: int) -> _SynthKeyItem:
        return self._keys[key]

    def note_on(self, channel: int, key: int, velocity: int):
        super().note_on(channel, key, velocity)
        item = self._get_item_for_key(key)
        item.begin()
        item.attack = self._attack
        item.sustain = self._sustain
        item.decay = self._decay
        item.amp = float(velocity) * ONE_OVER_128

    def note_off(self, channel: int, key: int, velocity: int):
        super().note_off(channel, key, velocity)
        self._get_item_for_key(key).queue_end()

    def _make_envelope(
        self, buffer_size: int, key_item: _SynthKeyItem
    ) -> NDArray[np.float32]:
        buffer: NDArray[np.float32]

        if key_item.attack:
            duration = cast(int, key_item.duration)
            buffer = np.linspace(
                duration / key_item.attack,
                min(1.0, (duration + buffer_size) / key_item.attack),
                buffer_size,
            )

            if duration + buffer_size > key_item.attack:
                key_item.duration = 0
                key_item.attack = None

        elif key_item.sustain:
            buffer = np.ones(buffer_size, dtype=np.float32)

            if cast(int, key_item.duration) + buffer_size >= key_item.sustain:
                key_item.duration = 0
                key_item.sustain = None

        elif key_item.decay:
            duration = cast(int, key_item.duration)
            buffer = np.linspace(
                1.0 - (duration / key_item.decay),
                1.0 - min(1.0, (duration + buffer_size) / key_item.decay),
                buffer_size,
            )

            if duration + buffer_size >= key_item.decay:
                key_item.duration = None

        else:
            buffer = np.ones(buffer_size, dtype=np.float32)

        return buffer

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

        with self._lock:
            for item in self._keys:
                # not item.is_alive(), fixes type issue below
                if item.duration is None:  # remember: 0 is falsy
                    continue

                buffer += self._oscillator._make_buffer_for_key(
                    frame_count, item.t, item.step, 0.0, item.amp
                )
                buffer *= self._make_envelope(frame_count, item)

                item.t += item.step * float(frame_count)
                if item.duration is not None:
                    item.duration += frame_count

        return (np.clip(buffer, -1.0, 1.0).tobytes(), pa.paContinue)
