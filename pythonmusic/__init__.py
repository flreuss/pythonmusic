from .constants import *
from .helpers import *
from .io import *
from .music import *
from .play import *
from .util import *

# This ensures that the fluid synth parts of this library are only imported if
#  fluidsynth is installed. The binding library will check and returns the error
#  message below if not installed.

# TODO: find a more elegant solution for this
try:
    from .synth import *
except ImportError as e:
    if str(e) == "Couldn't find the FluidSynth library.":
        pass
    else:
        raise e
