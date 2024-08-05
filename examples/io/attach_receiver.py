"""
# Create a Midi Receiver Object

This example shows how to create a midi receiver that attaches to a specific midi
source. Add custom callbacks to react to specific midi messages.

# Usage
This script attaches to a specific midi source. This could be a midi-capable 
keyboard or DAW output port. Use functionality shown below to list available 
sources.

Alternative, this module also provides other examples that can be used to send
midi messages. See `host_sender.py`.

# Dependencies
Make sure that python packages `mido` and `python-rtmidi` are installed in your
virtual environment.
"""

from time import sleep
from typing import NoReturn

from pythonmusic import get_midi_senders
from pythonmusic import MidiMessage, MidiReceiver, MATCH_ALL
from pythonmusic import NOTE_ON, NOTE_OFF


def wait():
    while True:
        sleep(1)


def on_note_on(msg: MidiMessage):
    assert msg.type == NOTE_ON
    print(f"Note on  - pitch: {msg['note']}, velocity: {msg['velocity']}")


def on_note_off(msg: MidiMessage):
    assert msg.type == NOTE_OFF
    print(f"Note off - pitch: {msg['note']}, velocity: {msg['velocity']}")


def on_any_message(msg: MidiMessage):
    print(f"received message of type {msg.type}")


if __name__ == "__main__":
    # get available midi senders
    senders = get_midi_senders()
    # if non are found, print error message and exit
    if len(senders) == 0:
        print("No open midi senders found")
        exit(1)
    # we have at least one sender, we continue

    # next, we need to choose a sender
    name: str | None = None
    # if we have more than one option, ask the user to choose one
    if len(senders) != 1:
        while name is None:
            try:
                print("Please choose a sender:")
                for index, sender in enumerate(senders):
                    print(f" [{index}]: {sender}")
                i = int(input("(int) > "))

                if i in range(0, len(senders)):
                    name = senders[i]
                else:
                    print("Index is out of range\n")
            except ValueError:
                print("Not an integer\n")
                pass
    else:
        name = senders[0]
        print("Only one port available")

    print(f"Chosen port: {name}")

    # to create the MidiReceiver we use the `attach` class function instead of
    # creating a host
    receiver = MidiReceiver.attach(name)
    print("Attached to port")

    # you can also enable debug printing by uncommenting the following line
    receiver.prints_messages_to_stdout = True

    # assuming that the receiver connected successfully, we can now add callbacks
    # that react to midi messages
    receiver.add_callback(MATCH_ALL, on_any_message)
    receiver.add_callback(NOTE_ON, on_note_on)
    receiver.add_callback(NOTE_OFF, on_note_off)

    # receivers run in the background, so keep the main thread running
    try:
        print(receiver._callbacks)
        wait()
    except KeyboardInterrupt:
        print("End")
