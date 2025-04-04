"""
# Create a virtual midi sender object.

This example shows how to create a virtual midi output that other applications
can attach to and receive messages from.

## Usage
This script opens a virtual midi port that is visible to other applications.
This could be a DAW or `MidiIn` from this library.
"""

from random import uniform as randf
from time import sleep

from pythonmusic import *

if __name__ == "__main__":
    # define a name for your receiver
    MIDI_PORT = "MyExampleMidiSender"

    # The name above is passed to the OS. Depending on your platform, this may
    # not be the name under which you will find the port. This library provides
    # methods that can search for similarly named ports.
    # see `find_midi_outputs()`.

    # create a midi output
    output = MidiOut(MIDI_PORT, virtual=True)
    output_label = find_midi_output(MIDI_PORT)
    print(f'Started midi output as "{output_label}')

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
