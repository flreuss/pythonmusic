"""
Midi Messages

A thin wrapper around mido' MIDI messages.
"""

from mido.messages import Message


# TODO: is this neccessary, or should this just expose mido directly

# This class is a thin wrapper around mido's Message class. The idea is
# to simplyfy and reduce the exposed api.


class MidiMessage:
    def __init__(self, type: str, **args) -> None:
        self._message = Message(type, False, **args)
