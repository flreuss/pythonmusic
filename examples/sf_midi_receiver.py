from time import sleep

from pythonmusic import *

# define sound font path and name for midi port
SF_PATH = "gm.sf2"
MIDI_PORT = "SfMidi"

# create sound font target object
sf_target = SfTarget(SF_PATH)

# create a midi player that we pass the sf target to
player = MidiInPlayer(sf_target, MIDI_PORT, True)

print("Started midi in")

# The player runs in the background, received midi messages and passes them to
# the target.
# Because the player is not blocking, we need to keep the thread alive, or the
# program may end

# wrap the loop in a try/except block to surpress errors from interrupting with
# ctrl+c
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print("Stopped midi in")
