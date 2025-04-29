"""
# Create a midi sender object.

This example shows how to create a midi sender object that attaches to a midi
input port and sends messages.

## Usage
This script attaches to a midi input port. This could be a digital piano or open
input port of some DAWs.

To create a midi output port that other midi inputs can see and attach to, see
`virtual_midi_out.py`.
"""

from random import uniform as randf
from time import sleep

from pythonmusic import *

if __name__ == "__main__":
    # get available midi inputs
    # this will ask the user to chose one, if multiple are present
    input = input_user_prompt()

    # if input is none, no port was available
    if input is None:
        print("No open midi input ports found")
        exit(1)

    print(f"Attaching to port {input}")

    # create a midi output port that receives messages from the chosen midi
    # input port
    # this port is not virtual; use a virtual port to create an input port that
    # others can attach to
    # see `virtual_midi_out.py` for more information
    output = MidiOut(input)  # virtual = False

    # after connecting send midi messages
    message_on = Message.new_note_on(0, C4, MF)
    message_off = Message.new_note_off(0, C4, MF)
    while True:
        try:
            print("Sending NOTE_ON")
            output.send_message(message_on)
            sleep(randf(0.1, 0.8))

            print("Sending NOTE_OFF")
            output.send_message(message_off)
            sleep(randf(0.1, 0.3))
        except KeyboardInterrupt:
            print("closed output")
            break
