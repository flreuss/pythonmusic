"""
# Create a Midi Sender Object

This example shows how to create a midi sender object that attaches to a specific
midi input port.

# Usage
This script attaches to a specific midi input port. This could be the open midi
input port that some DAWs provide (i.e. Logic Pro X).

Alternatively, This module also provides other examples that can be used to
receive midi messages. See `host_receiver.py`.

# Dependencies
Make sure that python packages `mido` and `python-rtmidi` are installed in your
virtual environment.
"""

from time import sleep
from random import uniform as random

from pythonmusic import MidiMessage, MidiSender, get_midi_receivers
from pythonmusic import NOTE_ON, NOTE_OFF


if __name__ == "__main__":
    # get available midi receivers
    receivers = get_midi_receivers()
    # if non are found, print error message and exit
    if len(receivers) == 0:
        print("No open midi receivers found")
        exit(1)
    # we have at least one receiver, we continue

    # next, we need to choose a receiver
    name: str | None = None
    # if we have more than one option, ask the user to choose one
    if len(receivers) != 1:
        while name is None:
            try:
                print("Please choose a reciever:")
                for index, receiver in enumerate(receivers):
                    print(f" [{index}]: {receiver}")
                i = int(input("(int) > "))

                if i in range(0, len(receivers)):
                    name = receivers[i]
                else:
                    print("Index is out of range\n")
            except ValueError:
                print("Not an integer\n")
                pass
    else:
        name = receivers[0]
        print("Only one port available")

    print(f"Chosen port: {name}")
    print("Attaching to port")

    # to create the MidiSender we use the `attach` class function instead of
    # creating a host
    sender = MidiSender.attach(name)

    # assuming that the sender connected successfully, we can now send messages
    # to the reciever
    on = MidiMessage(NOTE_ON, note=60)
    off = MidiMessage(NOTE_OFF, note=60)
    while True:
        try:
            print("Sending note on")
            sender.send_message(on)
            sleep(random(0.1, 0.8))
            print("Sending note off")
            sender.send_message((off))
            sleep(random(0.1, 0.3))
        except KeyboardInterrupt:
            print("End")
            break
