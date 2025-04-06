from threading import Lock
from typing import Mapping, Optional

import numpy as np
import pyaudio as pa

from pythonmusic.play.audio_steam import AudioStream
from pythonmusic.play.target import Target

__all__ = ["Oscillator", "SynthesizerTarget"]


class Oscillator:
    def __init__(self, amp: float, freq: float):
        self._n: int = 0

        # CONTINUE: implement osc, synth, test audiostream for metronome

    def reset(self):
        self._n = 0


class SynthesizerTarget(AudioStream, Target):
    pass
