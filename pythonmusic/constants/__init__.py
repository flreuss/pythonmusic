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

PPQ: int = 960
"""Default ticks per quarter."""

PERCUSSION_CHANNEL: int = 9
"""
Midi channel constant for the percussion channel.

Instead of notes, most midi synthesizers will play persussion instruments for
notes send on this channel.

In the midi standard, the percussion channel is `10`. This library uses 
zero-indexed channel values, so the library-internal number is `9`.
"""
