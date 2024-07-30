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

from time import sleep

from pythonmusic import MidiMessage, MidiReceiver
from pythonmusic import NOTE_ON, NOTE_OFF


def on_note_on(msg: MidiMessage):
    assert msg.type == NOTE_ON
    print(f"Note on  - pitch: {msg['pitch']}, velocity: {msg['velocity']}")


def on_note_off(msg: MidiMessage):
    assert msg.type == NOTE_OFF
    print(f"Note off - pitch: {msg['pitch']}, velocity: {msg['velocity']}")


if __name__ == "__main__":
    # create a new midi receiver
    receiver = MidiReceiver("ExampleMidiReceiver")
    print(f"Creates midi receiver: {receiver.name}")

    # add callbacks to midi events
    receiver.add_callback(NOTE_ON, on_note_on)
    receiver.add_callback(NOTE_OFF, on_note_off)

    # receivers run in the background, so keep the main thread running
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Closed midi port")
