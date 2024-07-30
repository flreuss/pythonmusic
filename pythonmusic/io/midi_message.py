"""
Midi Messages

A thin wrapper around mido' MIDI messages.
"""

from mido.messages import Message as MidiMessage


# TODO: is this neccessary, or should this just expose mido directly

# This class is a thin wrapper around mido's Message class. The idea is
# to simplyfy and reduce the exposed api.


# class MidiMessage:
#     def __init__(self) -> None:
#         self.raw: RawMessage | None = None
#
#     def __getitem__(self, key) -> Any:
#
#
#     @staticmethod
#     def from_raw(raw: RawMessage) -> "MidiMessage":
#         new = MidiMessage()
#         new.raw = raw
#         return new
