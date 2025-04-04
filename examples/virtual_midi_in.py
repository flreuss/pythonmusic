"""
# Create a virtual midi receiver object.

This example shows how to create a virtual midi input that other applications
can send midi message to. Add custom callbacks to respond to midi messages.

## Usage
This script opens a virtual midi port that is visible to other applications.
This could be a DAW or `MidiOut` from this library.

If you need to attach to an existing midi output, see `attach_midi_out.py`.
"""

from time import sleep

from pythonmusic import *


def on_note_on(message: Message):
    assert message.type() == NOTE_ON
    key = message.key
    velocity = message.velocity
    print(f"Note on  - key: {key}, velocity: {velocity}")


def on_note_off(message: Message):
    assert message.type() == NOTE_OFF
    key = message.key
    velocity = message.velocity
    print(f"Note off - key: {key}, velocity: {velocity}")


def on_any_message(message: Message):
    message_type = message.type()
    # note on and off is handled above, continue only if we have another event
    if message_type == NOTE_ON or message_type == NOTE_OFF:
        return

    print(f"received message of type {message_type}")


if __name__ == "__main__":
    # define a name for your receiver
    MIDI_PORT = "MyExampleMidiReceiver"

    # The name above is passed to the OS. Depending on your platform, this may
    # not be the name under which you will find the port. This library provides
    # methods that can search for similarly named ports.
    # see `find_midi_inputs()`.

    # create a midi input
    input = MidiIn(MIDI_PORT, virtual=True)
    input_label = find_midi_input(MIDI_PORT)
    print(f'Started midi input as "{input_label}"')

    # you can enable printing of incoming message to console by setting
    # `input.prints_messages = True`

    # add callbacks for note events
    input.set_callback(NOTE_ON, on_note_on)
    input.set_callback(NOTE_OFF, on_note_off)
    # if `None` is passed instead of an explicit event, it will respond to all
    # messages
    input.set_callback(None, on_any_message)

    # callbacks execute in the background, so we need to block the main thread
    # while we receive messages
    # you can end with a KeyboardInterrupt (ctrl+c)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
