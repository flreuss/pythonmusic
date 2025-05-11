from threading import Thread
from time import sleep, time
from typing import Callable, Optional

from pythonmusic.constants import (
    A4,
    A5,
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
    P,
)
from pythonmusic.play.synthesizer import Oscillator, SineOscillator, SynthesizerTarget
from pythonmusic.play.target import Target
from pythonmusic.util import bpm_to_sec

__all__ = ["Metronome"]

# default values for metronome
VELOCITY: int = P
OSC: type[Oscillator] = SineOscillator
ATTACK: Optional[float] = 0.01
SUSTAIN: Optional[float] = None
DECAY: Optional[float] = 0.2


def _make_default_target() -> Target:
    return SynthesizerTarget(
        OSC(),
        ATTACK,
        SUSTAIN,
        DECAY,
        AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    )


class Metronome:
    """
    A simple metronome that allows you to run code on every beat.

    This class accepts a callback function that is executed on every beat.
    To add a callback, define a function and pass it to the constructor:

    .. code-block:: python

        def my_callback():
            # some code
            print("beat")

        metronome = Metronome(120, 3, my_callback)

    Optionally, the callback may return a `bool` that indicated if the metronome
    should continue to play.

    You can mute the metronome by setting the ``target`` parameter to
    :obj:`EmptyTarget <pythonmusic.play.EmptyTarget>`:

    .. code-block:: python

        metronome = Metronome(120, 3, EmptyTarget())

    Args:
        bpm (float): Beat in beats per minute
        beat (int): The beat of the time signature
        callback (Optional[Callable[[], Optional[bool]]]): An optional callback
            that is executed on every beat
        target (Optional[Target]): An alternative target to play the beat on
    """

    def __init__(
        self,
        bpm: float,
        beat: int = 4,
        callback: Optional[Callable[[], Optional[bool]]] = None,
        target: Optional[Target] = None,
    ):
        self._beat_duration: float = bpm_to_sec(bpm)
        self._callback = callback

        self._synth: Target = target or _make_default_target()

        self._off_beat: int = A4
        self._on_beat: int = A5
        self._beat: int = beat
        self._current_beat: int = 0
        self._velocity = VELOCITY

    def synth(self) -> Target:
        """Returns the metronome's target."""
        return self._synth

    def set_callback(self, callback: Optional[Callable[[], None]]):
        """Updates the metronome's callback."""
        self._callback = callback

    def set_on_beat(self, v: int):
        """Updates the key pitch for on beats notes."""
        self._off_beat = v

    def set_off_beat(self, v: int):
        """Updates the key pitch for off beats notes."""
        self._off_beat = v

    def set_beat(self, beat: int):
        """
        Updates the metronome's beat and resets.
        """
        self._beat = beat
        self._current_beat = 0

    def current_beat(self) -> int:
        """Returns the current beat."""
        return self._current_beat

    def set_velocity(self, v: int):
        """Updates the velocity with which the metronome's sound is played."""
        self._velocity = v

    def start(self):
        """
        Starts the metronome in the background.

        Calls the callback every beat until it returns `False`.

        Keep in mind that you will need to block the main thread.
        """
        thread = Thread(target=self._run)
        thread.start()

    def block(self):
        """
        Starts the metronome and blocks until the callback returns `False`.
        """
        self._run()

    def _run(self):
        should_continue = True
        while should_continue:
            # lets not users change this during sleep
            sleep_duration = self._beat_duration

            key = self._on_beat if self._current_beat == 0 else self._off_beat

            self._synth.note_on(0, key, self._velocity)

            begin_callback = time()
            # python's truthy- and falsyness
            if self._callback:
                response = self._callback()
                if response is not None:
                    should_continue = response

            # subtract callback execution time
            sleep(sleep_duration - (time() - begin_callback))
            self._synth.note_off(0, key, 0)

            self._current_beat += 1
            if self._current_beat >= self._beat:
                self._current_beat = 0
