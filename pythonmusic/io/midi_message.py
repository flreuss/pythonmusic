"""
Midi Messages

A thin wrapper around mido' MIDI messages.
"""

from mido.messages import Message as _MidoMessage


# TODO: is this neccessary, or should this just expose mido directly

# This class is a thin wrapper around mido's Message class. The idea is
# to simplyfy and reduce the exposed api.


class MidiMessage:
    def __init__(self, raw: _MidoMessage) -> None:
        raw_dict = raw.dict()
        self.type = raw_dict["type"]
        ...
