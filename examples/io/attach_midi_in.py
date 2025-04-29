"""
# Create a midi receiver object.

This example shows how to create a midi receiver that attaches to a midi output
source and received messages. Add custom callbacks to respond to incoming midi
messages.

## Usage
This script attaches to a midi output source. This could be a midi-capable
keyboard, digital piano, or DAW.

To create a midi input port that other midi outputs can see and attach to, see
`attach_midi_in.py`.
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
    # get available midi outputs
    # this will ask the user to choose one, if multiple are available
    output = output_user_prompt()

    # if output is none, no port was available
    if output is None:
        print("No open midi output ports found")
        exit(1)

    print(f"Attaching to port {output}")

    # create a midi input port that receives messages from the chosen midi
    # output port
    # this port is not virtual; use a virtual port to create an input port that
    # others can attach to
    # see `virtual_midi_in.py` for more information
    input = MidiIn(output)  # virtual = False

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
