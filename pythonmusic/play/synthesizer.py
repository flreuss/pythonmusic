import math
from abc import ABC, abstractmethod
from enum import Enum
from queue import Empty, Queue
from typing import Mapping, Optional, override

import numpy as np
import pyaudio as pa
from numpy.typing import NDArray

from pythonmusic.constants import (
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
)
from pythonmusic.play.audio_stream import AudioStream
from pythonmusic.play.target import Target
from pythonmusic.util import (
    assert_range,
    key_to_frequency,
    samples_to_seconds,
    seconds_to_samples,
)

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


class SynthStage(Enum):
    IDLE = 0
    ATTACK = 1
    DECAY = 2
    SUSTAIN = 3
    RELEASE = 4


class SynthKeyItem:
    __slots__ = ("t", "step", "amp", "duration", "stage")

    def __init__(self, step: float):
        self.t = 0.0
        self.step = step
        self.amp = 1.0
        self.duration: int = 0
        self.stage: SynthStage = SynthStage.IDLE


class Oscillator(ABC):
    """
    A base class for oscillators.

    To create a class from this, implement the
    :meth:`sample() <pythonmusic.play.Oscillator.sample>`
    method.

    Oscillators should not store timing data internally, but rely on the
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
        return ((phase + t + (step * np.arange(buffer_size))) % 1.0) * amp


class SynthesizerTarget(AudioStream, Target):
    """
    A synthesizer target that generates sound from oscillators.

    The synthesizer uses an :obj:`oscillators <pythonmusic.play.Oscillator>` to
    create a base wave that is combined with an ADSR envelope, that you define
    by setting the ``attack``, ``decay``, ``sustain``, and ``release``
    parameters.

    The ``decay`` parameter requires a two-place tuple with the duration of the
    decay in first, and the amount of volume reduction in percent in the second.
    A tuple ``delay=(0.2, 0.75)`` would reduce the volume by 75% in 0.2 seconds.

    The ``sustain`` parameter defines the duration the note is held without
    change in envelope. You can pass ``None`` to keep the note playing until
    the note off event is received.

    Args:
        oscillator (Oscillator): An oscillator
        attack (float): Duration of attack in seconds
        decay (tuple[float, float]): Tuple containing delay duration in seconds
            and volume reduction in percent
        sustain (Optional[float]): Duration of sustain in seconds
        release (float): Duration of release in seconds
        sample_rate(int): Sample rate per second
        buffer_size(int): Sample buffer size
    """

    def __init__(
        self,
        oscillator: Oscillator,
        attack: float = 0.02,
        decay: tuple[float, float] = (0.0, 0.0),
        sustain: Optional[float] = None,
        release: float = 0.05,
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        super().__init__(1, sample_rate, buffer_size, pa.paFloat32)
        self._sample_rate = sample_rate
        self._buffer_size = buffer_size
        self._keys = list(
            map(
                lambda key: SynthKeyItem(
                    math.tau * key_to_frequency(key) / float(sample_rate)
                ),
                range(128),
            )
        )

        self._event_queue: Queue[tuple[int, int, bool]] = Queue()

        self._oscillator = oscillator

        assert attack >= 0.0
        assert decay[0] >= 0.0
        assert_range(decay[1], 0.0, 1.0)
        assert release >= 0

        self._attack: int = seconds_to_samples(attack, sample_rate)
        self._decay: int = seconds_to_samples(decay[0], sample_rate)
        self._decay_reduction: float = decay[1]
        self._sustain: Optional[int] = (
            seconds_to_samples(sustain, sample_rate) if sustain is not None else None
        )
        self._release: int = seconds_to_samples(release, sample_rate)

    @property
    def oscillator(self) -> Oscillator:
        return self._oscillator

    @oscillator.setter
    def oscillator(self, v: Oscillator):
        self._oscillator = v

    @property
    def attack(self) -> float:
        return samples_to_seconds(self._attack, self._sample_rate)

    @attack.setter
    def attack(self, v: float):
        self._attack = seconds_to_samples(v, self._sample_rate)

    @property
    def decay(self) -> float:
        return samples_to_seconds(self._decay, self._sample_rate)

    @decay.setter
    def decay(self, v: float):
        self._decay = seconds_to_samples(v, self._sample_rate)

    @property
    def decay_reduction(self) -> float:
        return self._decay_reduction

    @decay_reduction.setter
    def decay_reduction(self, v: float):
        assert_range(v, 0.0, 1.0)
        self._decay_reduction = v

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
    def release(self) -> float:
        return samples_to_seconds(self._release, self._sample_rate)

    @release.setter
    def release(self, v: float):
        self._release = seconds_to_samples(v, self._sample_rate)

    def sample_rate(self) -> int:
        """Returns the synth's sample rate."""
        return self._sample_rate

    def buffer_size(self) -> int:
        """Returns the synth's buffer size."""
        return self._buffer_size

    def is_playing(self, key: int) -> bool:
        """Returns `True` if a note for the given key is playing."""
        return self._keys[key].stage != SynthStage.IDLE

    def _get_item_for_key(self, key: int) -> SynthKeyItem:
        return self._keys[key]

    def _note_will_start(self, key: int, velocity: int):
        item = self._get_item_for_key(key)

        item.duration = 0
        item.stage = SynthStage.ATTACK
        item.amp = float(velocity) * ONE_OVER_128

    def _note_will_end(self, key: int):
        item = self._get_item_for_key(key)

        # if item has already ended or is in release, return
        if item.stage == SynthStage.IDLE or item.stage == SynthStage.RELEASE:
            return

        # otherwise skip stage to release
        item.duration = 0
        item.stage = SynthStage.RELEASE

    def _make_envelope(
        self, buffer_size: int, key_item: SynthKeyItem
    ) -> NDArray[np.float32]:
        match key_item.stage:
            case SynthStage.ATTACK:
                duration = float(key_item.duration)
                attack = float(self._attack)

                return np.linspace(
                    # start: progress of attack
                    duration / attack,
                    # stop: progress at buf end, clipped to 1.0
                    min(1.0, (duration + float(buffer_size)) / attack),
                    buffer_size,
                    dtype=np.float32,
                )

            case SynthStage.DECAY:
                duration = float(key_item.duration)
                decay = float(self._decay)

                return np.linspace(
                    # start: 1 - progress, (progress should never be > 1)
                    1.0 - (self._decay_reduction * (duration / decay)),
                    # stop: 1 - progress * decay reduction target
                    1.0
                    - (
                        self._decay_reduction
                        * min(1.0, (duration + float(buffer_size)) / decay)
                    ),
                    buffer_size,
                    dtype=np.float32,
                )

            case SynthStage.SUSTAIN:
                return np.full(
                    buffer_size, 1.0 - self._decay_reduction, dtype=np.float32
                )

            case SynthStage.RELEASE:
                duration = float(key_item.duration)
                release = float(self._release)
                sustain_level = 1.0 - self._decay_reduction

                return np.linspace(
                    # start: sustain level times progress of release
                    sustain_level - (sustain_level * (duration / release)),
                    # stop:
                    sustain_level
                    - (sustain_level * min(1.0, (duration + buffer_size) / release)),
                    buffer_size,
                    dtype=np.float32,
                )

        raise ValueError()

    def _update_key_item(self, key_item: SynthKeyItem):
        if key_item.stage == SynthStage.IDLE:
            return

        # we may need to skip stages, so this loops
        # just in case, count iterations, we should not exeede 2
        while True:
            match key_item.stage:
                case SynthStage.ATTACK:
                    # check if advance to next stage
                    if key_item.duration >= self._attack:
                        key_item.duration = 0
                        key_item.stage = SynthStage.DECAY
                        # do not break, let loop check again
                    else:
                        # still frames left in attack
                        break

                case SynthStage.DECAY:
                    # check if advance to next stage
                    if key_item.duration >= self._decay:
                        key_item.duration = 0
                        key_item.stage = SynthStage.SUSTAIN
                        # do not break, let loop check again
                    else:
                        # still frames left in attack
                        break

                case SynthStage.SUSTAIN:
                    # sustain may be None, aka. the note hold until ended
                    # in that case, this function does not ever advance to
                    # release, which is triggered by `_note_will_end`
                    if self._sustain is None:
                        break

                    if key_item.duration >= self._sustain:
                        key_item.duration = 0
                        key_item.stage = SynthStage.RELEASE
                        # do not break, but loop again
                    else:
                        # still frames left in attack
                        break

                case SynthStage.RELEASE:
                    if key_item.duration >= self._release:
                        key_item.duration = 0
                        key_item.stage = SynthStage.IDLE
                    # here, we break out in either case
                    break

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
            # retrieve note events
            try:
                while True:
                    item = self._event_queue.get(block=False)
                    if item[2]:
                        self._note_will_start(item[0], item[1])
                    else:
                        self._note_will_end(item[0])
            except Empty:
                pass

            for item in self._keys:
                # update key item stage
                self._update_key_item(item)

                # if item is not playing, continue
                if item.stage == SynthStage.IDLE:
                    continue

                buffer += (
                    self._oscillator._make_buffer_for_key(
                        frame_count, item.t, item.step, 0.0, item.amp
                    )
                    * BASE_AMP
                    * self._make_envelope(frame_count, item)
                )

                item.t += item.step * float(frame_count)
                item.duration += frame_count

        return (np.clip(buffer, -1.0, 1.0).tobytes(), pa.paContinue)

    # impl Target
    @override
    def note_on(self, channel: int, key: int, velocity: int):
        """:meta private:"""
        super().note_on(channel, key, velocity)
        self._event_queue.put((key, velocity, True))

    @override
    def note_off(self, channel: int, key: int, velocity: int):
        """:meta private:"""
        super().note_off(channel, key, velocity)
        self._event_queue.put((key, velocity, False))
