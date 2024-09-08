from typing import Self, Any, cast
from mido.messages import Message as RawMessage
from mido.messages.checks import Integral

__all__ = ["MidiMessage", "RawMessage"]

# This class is a thin wrapper around mido's Message class. The idea is
# to simplify and reduce the exposed api. This also allows type annotations.


class MidiMessage:
    """
    An object that represents a midi message.
    """

    __slots__ = "_raw"

    def __init__(self, type: str, **args) -> None:
        """
        Creates a new midi message.

        Args:
            type (str): The type of the midi message. See
                :mod:`pythonmusic.constants.messages` for more information.


                Continue here
        """
        self._raw = RawMessage(type, **args)

    def __str__(self):
        return self._raw.__str__()

    def __getitem__(self, key: str) -> Any:
        return self._raw.dict()[key]

    @property
    def type(self) -> str:
        return self._raw.dict()["type"]

    @property
    def time(self) -> float:
        return self._raw.time  # type: ignore [reportAttributeAccessIssue]

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
        return cls.from_raw(RawMessage.from_bytes(data, cast(Any, time)))

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
