"""
Midi Messages

A thin wrapper around mido' MIDI messages.
"""

from typing import Self, Any, cast as _cast
from mido.messages import Message as RawMessage
from mido.messages.checks import Integral


# TODO: is this neccessary, or should this just expose mido directly

# This class is a thin wrapper around mido's Message class. The idea is
# to simplyfy and reduce the exposed api. This also allows type annotations.


class MidiMessage:
    __slots__ = "_raw"

    def __init__(self, type: str, **args) -> None:
        self._raw = RawMessage(type, **args)

    def __str__(self):
        return self._raw.__str__()

    def __getitem__(self, key: str) -> Any:
        return self._raw.dict()[key]

    def __setitem__(self, key: str, value: Any):
        self._raw.dict()[key] = value

    @property
    def type(self) -> str:
        return self._raw.dict()["type"]

    @classmethod
    def _init_unsafe(cls) -> Self:
        # SAFETY: all fields must be initialised by caller
        return cls.__new__(cls)

    @classmethod
    def from_raw(cls, raw: RawMessage) -> Self:
        new = cls._init_unsafe()
        new._raw = raw
        return new

    @classmethod
    def from_bytes(cls, data: list[Integral], time: float | int = 0.0) -> Self:
        return cls.from_raw(RawMessage.from_bytes(data, _cast(Any, time)))

    def raw(self) -> RawMessage:
        """
        Returns the underlying raw message.

        This class is a thin wrapper around a `mido.Message` object. Use this
        function to access this object directly.
        """
        return self._raw

    def copy(self) -> "MidiMessage":
        raw_copy = self._raw.copy()
        return MidiMessage.from_raw(raw_copy)

    def bytes(self) -> list[int]:
        return self._raw.bytes()
