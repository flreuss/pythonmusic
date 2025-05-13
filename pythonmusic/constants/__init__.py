"""
This module defines several MIDI and music constants.
"""

from .articulations import *
from .chords import *
from .control_change import *
from .durations import *
from .dynamics import *
from .instruments import *
from .intervals import *
from .messages import *
from .meta import *
from .panning import *
from .percussion import *
from .pitches import *
from .scales import *
from .tempo import *

PERCUSSION_CHANNEL: int = 9
"""
Midi channel constant for the percussion channel.

Instead of notes, most midi synthesizers will play persussion instruments for
notes send on this channel.

In the midi standard, the percussion channel is `10`. This library uses 
zero-indexed channel values, so the library-internal number is `9`.
"""

# TODO: test if the constants below can be optimised; no need for high relolution

PPQ: int = 960
"""
Defines the default midi quarter resolution in ticks (pulses) per quarter note.
"""

AUDIO_STREAM_DEFAULT_SAMPLE_RATE: int = 44_100
"""
Defines the default sample rate for audio streams.
"""

AUDIO_STREAM_DEFAULT_BUFFER_SIZE: int = 512
"""
Defines the default buffer size for audio streams.
"""
