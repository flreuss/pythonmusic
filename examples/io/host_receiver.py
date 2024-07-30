"""
# Create a Midi Receiver Object

This example shows how to create a midi receiver that other applications can send
midi messages to. Add custom callbacks to react to specific midi messages.

# Usage
This script opens a midi port that should be visible to other applications. For 
instance, you could use a DAW to send your messages. Consult your DAW's manual 
for more information.

Alternatively, this module also provides other examples that can be used to send
midi messages. See `attach_sender.py`.

# Dependencies
Make sure that python packages `mido` and `python-rtmidi` are installed in your
virtual environment.
"""

from pythonmusic import MidiMessage, MidiReceiver
