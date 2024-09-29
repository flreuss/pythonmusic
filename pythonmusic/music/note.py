from copy import copy
from typing import Self, Any
from .phrase_element import PhraseElement
from pythonmusic.constants.articulations import LEGATO
from pythonmusic.constants.articulations import ACCENT
from pythonmusic.util import assert_range
from pythonmusic.constants.dynamics import MF
from pythonmusic.constants.pitches import REST

__all__ = ["Note"]


class Note(PhraseElement):
    """
    Notes represent a single musical note event. They are defined by their pitch,
    duration and dynamic. Use notes to create :obj:`pythonmusic.music.Phrase`
    and :obj:`pythonmusic.music.Chord`.

    Args:
        pitch (int): The note's pitch in midi representations. See
            :mod:`pythonmusic.constants.pitches`. Valid values are in range
            from `0` to `127`
        duration (float): The note's duration in quarter notes. See
            :mod:`pythonmusic.constants.durations`
        dynamic (int): The note's dynamic in range from `0` to `127`
        articulations: (list[int]): A list of articulations represented by
            bit sets. Use values defined in
            :mod:`pythonmusic.constants.articulations`
    """

    # Instructs python to store notes as a tuple. This can potentially reduce the
    # memory foot print of large scores.
    __slots__ = ("_pitch", "_dynamic", "_duration", "_articulation")

    def __init__(
        self,
        pitch: int,
        duration: float,
        dynamic: int = MF,
        articulations: list[int] = [],
    ) -> None:
        # Asserts that the given pitch and dynamic values can be represented
        # with a i8 / are in MIDI range. Pitch is allowed to be below 0 to
        # accommodate rests
        assert_range(pitch, -1, 127)
        assert_range(dynamic, 0, 127)

        self._pitch: int = pitch
        self._dynamic: int = dynamic
        self._duration: float = duration
        self._articulation: int = 0x0

        for articulation in articulations:
            self.add_articulation(articulation)

    def __eq__(self, other: Any) -> bool:
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
        """Pitch of the note."""
        return self._pitch

    @pitch.setter
    def pitch(self, new_value):
        assert_range(new_value, -1, 127)
        self._pitch = new_value

    @property
    def dynamic(self) -> int:
        """Dynamic of the note."""
        return self._dynamic

    @dynamic.setter
    def dynamic(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._dynamic = new_value

    @property
    def duration(self) -> float:
        """Duration of the note."""
        return self._duration

    @duration.setter
    def duration(self, new_value: int):
        self._duration = new_value

    def is_note(self) -> bool:
        """
        Returns `True` if the element is a note.

        .. note:: Always returns `True`.
        """
        return True

    def is_chord(self) -> bool:
        """
        Returns `True` if the element is a chord.

        .. note:: Always returns `False`.
        """
        return False

    def add_articulation(self, articulation: int):
        """
        Adds the given articulation to the note.

        Args:
            articulation (int): A bitset representing a note's articulation. Use
                a constant from :mod:`pythonmusic.constants.articulations`.
        """
        self._articulation |= articulation

    def remove_articulation(self, articulation: int):
        """
        Removes the given articulation from the note.

        Use the constants defined in :mod:`pythonmusic.constants.articulations`.

        Args:
            articulation (int): Articulation to add
        """
        self._articulation &= ~articulation

    def has_articulation(self, articulation: int) -> bool:
        """
        Returns `True` if this note has the given articulation.

        Args:
            articulation (int): A bitset representing a note's articulation. Use
                a constant from :mod:`pythonmusic.constants.articulations`

        Returns:
            bool: `True` if note has articulation
        """
        return self._articulation & articulation == articulation

    def with_legato(self) -> Self:
        """
        Returns this note with added legato.

        Returns:
            Note: This note with legato
        """
        note = copy(self)
        note.add_articulation(LEGATO)
        return note

    def with_accent(self) -> Self:
        """
        Returns this note with added accent.

        Returns:
            Note: This note with accent
        """
        note = copy(self)
        note.add_articulation(ACCENT)
        return note

    def is_rest(self) -> bool:
        """Returns `True` if this note is a rest."""
        return self._pitch == REST

    def as_rest(self) -> Self:
        """
        Returns a rest with this note's duration.

        Returns:
            Note: A rest with this note's duration
        """
        rest = copy(self)
        rest.pitch = REST
        return rest

    @classmethod
    def rest(cls, duration: float) -> Self:
        """
        Constructs a rest from the given duration.

        Args:
            duration (float): The duration of the rest

        Returns:
            Note: A rest with the given duration
        """
        return cls(REST, duration, 0)
