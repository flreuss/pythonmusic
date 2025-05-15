"""
Create a SynthesizerTarget and play inputs from an external midi keybaord.
"""

from pythonmusic import *

# get your midi device
midi_device = input_user_prompt()

# if input_user_prompt() return `None`, no midi devices were found
if midi_device is None:
    print("no midi input devices found")
    exit(1)

# setup synth target
osc = SineOscillator()  # any Oscillator
attack = 0.05  # attack for 0.05 seconds
decay = (2.0, 0.9)  # decay sound by 90% in 2 seconds
sustain = None  # sustain sound until note off is received
release = 0.5  # release note for 0.5 seconds

synth = SynthesizerTarget(osc, attack, decay, sustain, release)

# setup midi player
player = MidiInPlayer(synth, midi_device)

# the player runs in the background, so block the script to prevent Python
# from exiting
block()
