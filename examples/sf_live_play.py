"""
Connect to an external midi device, such as a midi keyboard or digital piano,
and play input on a target.
"""

from pythonmusic import *

# path to sound font file
SF_PATH = "path/to/file.sf2"

# get your midi device
midi_device = input_user_prompt()

# if input_user_prompt() return `None`, no midi devices were found
if midi_device is None:
    print("no midi input devices found")
    exit(1)

# setup a target to play messages on
target = SfTarget(SF_PATH)
target.set_instrument(0, ACOUSTIC_GRAND_PIANO)
# any target will work here

# create a midi in player with that target to receive messages
player = MidiInPlayer(target, midi_device, False)

# to prevent the script from running out, block the thread
block()
