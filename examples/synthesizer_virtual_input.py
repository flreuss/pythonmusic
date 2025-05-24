"""
Host a midi in that plays incoming messages on a SynthTarget.
"""

from pythonmusic import *

# name your port
PORT = "PythonMusic Example Input"

# create synth target
osc = SineOscillator()  # any Oscillator
attack = 0.05  # attack for 0.05 seconds
decay = (2.0, 0.9)  # decay sound by 90% in 2 seconds
sustain = None  # sustain sound until note off is received
release = 0.5  # release note for 0.5 seconds

synth = SynthesizerTarget(osc, attack, decay, sustain, release)

# setup midi in player (virtual)
player = MidiInPlayer(synth, PORT, True)  # set virtual to true

# the player is now visible to other midi applications

# the player runs in the background, so block the script to prevent Python
# from exiting
block()


# You can test this by attaching from another PythonMusic process with the
# following code
#
# from time import sleep
#
# from pythonmusic import *
#
# input = input_user_prompt()
# if input is None:
#     print("no input found")
#     exit(1)
#
# port = MidiOut(input, False)
#
# port.send_message(Message.new_note_on(0, C4, MF))
# sleep(1)
# port.send_message(Message.new_note_off(0, C4, MF))
# sleep(0.5)
