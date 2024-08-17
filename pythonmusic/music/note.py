from copy import copy as _copy
import typing as _typing
from .phrase_element import PhraseElement
from pythonmusic.constants.articulations import LEGATO as _LEGATO
from pythonmusic.constants.articulations import ACCENT as _ACCENT
from pythonmusic.util import assert_range as _assert_range
from pythonmusic.constants.dynamics import MF as _MF
from pythonmusic.constants.pitches import REST as _REST


class Note(PhraseElement):
    """
    Notes represent a single musical note event. They are defines by their pitch,
    duration and dynamic.
    """

    # Instructs python to store notes as a tuple. This can potentially reduce the
    # memory foot print of large scores.
    __slots__ = ("_pitch", "_dynamic", "_duration", "_articulation")

    def __init__(
        self,
        pitch: int,
        duration: float,
        dynamic: int = _MF,
        articulations: list[int] = [],
    ) -> None:
        # Asserts that the given pitch and dynamic values can be represented
        # with a i8 / are in MIDI range. Pitch is allowed to be below 0 to
        # accommodate rests
        _assert_range(pitch, -1, 127)
        _assert_range(dynamic, 0, 127)

        self._pitch: int = pitch
        self._dynamic: int = dynamic
        self._duration: float = duration
        self._articulation: int = 0x0

        for articulation in articulations:
            self.add_articulation(articulation)

    def __eq__(self, other: _typing.Any) -> bool:
        if not isinstance(other, Note):
            return False
        return (
            self._pitch == other._pitch
            and self._dynamic == other._dynamic
            and self._duration == other._duration
            and self._articulation == other._articulation
        )

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

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, new_value: int):
        self._duration = new_value

    def is_note(self) -> bool:
        return True

    def is_chord(self) -> bool:
        return False

    def add_articulation(self, articulation: int):
        """
        Adds the given articulation to the note.

        Use the constants defined in `pythonmusic.constants.articulations`.
        """
        self._articulation |= articulation

    def remove_articulation(self, articulation: int):
        """
        Removes the given articulation from the note.

        Use the constants defined in `pythonmusic.constants.articulations`.
        """
        self._articulation &= ~articulation

    def has_articulation(self, articulation: int) -> bool:
        """
        Returns `True` if this note has the given articulation.

        Use the constants defined in `pythonmusic.constants.articulations`.
        """
        return self._articulation & articulation == articulation

    def with_legato(self) -> _typing.Self:
        """
        Returns this note with added legato.
        """
        note = _copy(self)
        note.add_articulation(_LEGATO)
        return note

    def with_accent(self) -> _typing.Self:
        """
        Returns this note with added accent.
        """
        note = _copy(self)
        note.add_articulation(_ACCENT)
        return note

    def is_rest(self) -> bool:
        """Returns `True` if this note is a rest."""
        return self._pitch == _REST

    def as_rest(self) -> _typing.Self:
        """Returns a rest with this notes duration."""
        rest = _copy(self)
        rest.pitch = _REST
        return rest

    @staticmethod
    def rest(duration: float) -> "Note":
        """Constrcuts a rest from the given duration."""
        return Note(_REST, duration, 0)
