from threading import Thread
from time import sleep, time
from typing import Callable, Optional

from pythonmusic.constants import (
    A4,
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
    P,
)
from pythonmusic.music import Note
from pythonmusic.play.synthesizer import Oscillator, SineOscillator, SynthesizerTarget
from pythonmusic.play.target import Target
from pythonmusic.util import bpm_to_sec

__all__ = ["Metronome"]

# default values for metronome
KEY: int = A4
VELOCITY: int = P
OSC: type[Oscillator] = SineOscillator
ATTACK: Optional[float] = 0.01
SUSTAIN: Optional[float] = None
DECAY: Optional[float] = 0.2


class Metronome:
    def __init__(
        self,
        bpm: float,
        callback: Optional[Callable[[], Optional[bool]]],
        target: Optional[Target] = None,
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        self._beat_duration: float = bpm_to_sec(bpm)
        self._callback = callback

        self._synth: Target = (
            target
            if target
            else SynthesizerTarget(
                OSC(), ATTACK, SUSTAIN, DECAY, sample_rate, buffer_size
            )
        )

        self._key: int = KEY
        self._velocity = VELOCITY

    def synth(self) -> Target:
        """Returns the metronome's target."""
        return self._synth

    def set_callback(self, callback: Optional[Callable[[], None]]):
        """Updates the metronome's callback."""
        self._callback = callback

    def set_key(self, v: int):
        """Updates the pitch on which the metronome's sound is played on."""
        self._key = v

    def set_velocity(self, v: int):
        """Updates the velocity with which the metronome's sound is played."""
        self._velocity = v

    def start(self):
        """
        Starts the metronome in the background.

        Calls the callback every beat until it returns `False`.

        Keep in mind that you will need to block the main thread.
        """
        thread = Thread(target=self.block)
        thread.start()

    def block(self):
        """
        Starts the metronome and blocks until the callback returns `False`.
        """
        should_continue = True
        while should_continue:
            # lets not users change this during sleep
            key = self._key
            sleep_duration = self._beat_duration

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
