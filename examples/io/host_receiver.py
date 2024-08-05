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
    print(f"Note on  - pitch: {msg['note']}, velocity: {msg['velocity']}")


def on_note_off(msg: MidiMessage):
    assert msg.type == NOTE_OFF
    print(f"Note off - pitch: {msg['note']}, velocity: {msg['velocity']}")


if __name__ == "__main__":
    # define a name for the reciever
    name = "ExampleMidiReceiver"

    # Keep in mind that, depending on your platform, the receiver may not show
    # up under its given name. On Linux, for example, the midi reciever below
    # may be listed as "RtMidiIn Client:ExampleMidiReceiver 128:0". If so, you
    # will have to retrieve the actual name from the system. See
    # `pythonmusic.io.get_midi_receivers()`

    # create a new midi receiver
    print(f'Starting midi reciever as "{name}"')
    receiver = MidiReceiver(name)

    # you can also enable debug printing by uncommenting the following line
    # receiver.prints_messages_to_stdout = True

    # add callbacks to midi events
    receiver.add_callback(NOTE_ON, on_note_on)
    receiver.add_callback(NOTE_OFF, on_note_off)

    # receivers run in the background, so keep the main thread running
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Closed midi port")
