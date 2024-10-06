from typing import Self, Any, cast
from mido.messages import Message as RawMessage
from mido.messages.checks import Integral

__all__ = ["MidiMessage", "RawMessage"]

# This class is a thin wrapper around mido's Message class. The idea is
# to simplify and reduce the exposed api. This also allows type annotations.


class MidiMessage:
    """
    An object that represents a midi message.

    Args:
        type (str): The type of the midi message. See
            :mod:`pythonmusic.constants.messages` for more information.
        **kwargs: Parameters needed to construct specific midi messages. See
            :doc:`Midi Messages <../appendix/midi>`.
    """

    __slots__ = "_raw"

    def __init__(self, type: str, **kwargs) -> None:
        self._raw = RawMessage(type, **kwargs)

    def __str__(self):
        return self._raw.__str__()

    def __getitem__(self, key: str) -> Any:
        return self._raw.dict()[key]

    def __lt__(self, other: Self) -> bool:
        return self.time < other.time

    @property
    def type(self) -> str:
        """
        The type of this midi message.
        """
        return self._raw.dict()["type"]

    @property
    def time(self) -> float:
        """
        The time offset of the message from the beginning.
        """
        return self._raw.time  # type: ignore [reportAttributeAccessIssue]

    @classmethod
    def from_raw(cls, raw: RawMessage) -> Self:
        """
        Creates a new midi message from the given raw message.

        Args:
            raw (RawMessage): A raw message from which to construct
        """
        new = cls.__new__(cls)
        new._raw = raw
        return new

    @classmethod
    def from_bytes(cls, data: list[Integral], time: float | int = 0.0) -> Self:
        """
        Creates a new midi message from the given list of data.

        This allows to construct midi messages from their contents in byte
        format.

        Returns:
            MidiMessage: The constructed message
        """
        return cls.from_raw(RawMessage.from_bytes(data, cast(Any, time)))

    def raw(self) -> RawMessage:
        """
        Returns the underlying raw message.

        Returns:
            RawMessage: This messages raw representation.
        """
        return self._raw

    def copy(self) -> Self:
        """
        Returns a (deep) copy of this message.

        Returns:
            MidiMessage: A new message with this message's contents
        """
        raw_copy = self._raw.copy()
        return self.from_raw(raw_copy)

    def bytes(self) -> list[int]:
        """
        Returns this message in byte format.
        """
        return self._raw.bytes()
