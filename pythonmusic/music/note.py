from copy import deepcopy as _deepcopy
import typing as _typing
from pythonmusic.util.checks import assert_range as _assert_range
from pythonmusic.constants.dynamics import MF as _MF
from pythonmusic.constants.pitches import REST as _REST


class Note:
    """
    Notes represent a single musical note event. They are defines by their pitch,
    duration and dynamic.
    """

    # Instructs python to store notes as a tuple. This can potentially reduce the
    # memory foot print of large scores.
    __slots__ = ("_pitch", "_dynamic", "duration")

    def __init__(self, pitch: int, duration: float, dynamic: int = _MF) -> None:
        # Asserts that the given pitch and dynamic values can be represented
        # with a i8 / are in MIDI range. Pitch is allowed to be below 0 to
        # accommodate rests
        _assert_range(pitch, -1, 127)
        _assert_range(dynamic, 0, 127)

        self._pitch: int = pitch
        self._dynamic: int = dynamic
        self.duration: float = duration

    def __str__(self) -> str:
        return f"Note({self._pitch}, {self.duration}, {self._dynamic})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Note):
            return (
                self._pitch == other._pitch
                and self._dynamic == other._dynamic
                and self.duration == other.duration
            )
        return False

    # properties here assert that pitch and dynamic are never set to an invlaid
    # value
    @property
    def pitch(self) -> int:
        return self._pitch

    @pitch.setter
    def pitch(self, new_value):
        _assert_range(new_value, -1, 127)
        self._pitch = new_value

    @property
    def dynamic(self) -> int:
        return self._dynamic

    @dynamic.setter
    def dynamic(self, new_value: int):
        _assert_range(new_value, 0, 127)
        self._dynamic = new_value

    def is_rest(self) -> bool:
        """Returns `True` if this note is a rest."""
        return self._pitch == _REST

    def as_rest(self) -> _typing.Self:
        """Returns a rest with this notes duration."""
        rest = _deepcopy(self)
        rest.pitch = _REST
        return rest

    @staticmethod
    def rest(duration: float) -> "Note":
        """Constrcuts a rest from the given duration."""
        return Note(_REST, duration, 0)
