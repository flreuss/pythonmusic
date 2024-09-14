from typing import cast, Any, Self

from .note import Note
from .phrase_element import PhraseElement
from .note_collection import NoteCollection
from ..constants.dynamics import MF
from ..constants.intervals import OCTAVE

__all__ = ["Chord"]


class Chord(PhraseElement, NoteCollection):
    """
    A type that groups multiple notes together.

    Args:
        notes (list[Note]): A list of notes to add to the chord
    """

    __slots__ = "_notes"

    def __init__(self, notes: list[Note] = []) -> None:
        self._notes = []
        self.add_notes(cast(list[PhraseElement], notes))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Chord):
            return False

        length = self.length()
        if length != len(other.notes):
            return False

        for i in range(length):
            if self.notes[i] != other.notes[i]:
                return False

        return True

    def length(self) -> int:
        """
        Returns the number of notes in the chord.

        .. note:: Only checks for top level entries. Embedded chord will not be
            counted recursively.

        Return:
            int: The count of notes in the chord
        """
        return len(self.notes)

    @classmethod
    def from_lists(
        cls,
        pitches: list[int],
        durations: list[float],
        dynamics: list[int],
    ) -> Self:
        """
        Creates a chord by adding notes created from their individual values.

        .. warning:: The length of the given lists must be equal. That is, each
            note must have a pitch, duration and dynamic.

        Args:
            pitches (list[int]): A list of pitches
            durations (list[int]): A list of durations
            dynamics (list[int]): A list of dynamics

        """
        chord = cls()
        chord.add_notes_by_lists(pitches, durations, dynamics)

        return chord

    @property
    def notes(self) -> list[PhraseElement]:
        """
        The notes within the chord.
        """
        return self._notes

    @notes.setter
    def notes(self, new_value: list[PhraseElement]):
        self._notes = new_value

    @property
    def duration(self) -> float:
        """The duration of the chord."""
        return self.max_duration() or 0.0

    def is_note(self) -> bool:
        """
        Returns `True` if this element is a note.

        .. note:: Always returns `False`.
        """
        return False

    def is_chord(self) -> bool:
        """
        Returns `True` if this element is a note.

        .. note:: Always returns `True`.
        """
        return True

    @classmethod
    def from_root(
        cls,
        root: int,
        intervals: list[int],
        duration: float,
        dynamic: int = MF,
        limit: int | None = None,
    ) -> Self:
        """Creates a chord from given intervals over a root note.

        Args:
            root (int): A root pitch
            intervals (list[int]) A list of intervals over the root note
            duration (float): The duration of the chord
            dynamic (int): The dynamic of the chord
            limit (int | None): The upperlimit of the chord. If given, repeats
                intervale over the root note until limit is reached, otherwise,
                repeats only once. Defaults to `None`

        Returns:
            The constructed chord.
        """
        notes: list[Note] = []
        # if no intervals are given, return empty chord
        if len(intervals) == 0:
            pass

        # if intervals are given, but no limit is defined, do not repeat the
        # intervals, i.e., just a simple chord
        elif limit is None:
            notes = [Note(root + interval, duration, dynamic) for interval in intervals]

        # otherwise keep adding intervals until the limit is reached
        else:
            current_octave_offset = 0
            current_interval_index = 0

            while True:
                # calculate pitch to add
                pitch = (
                    root
                    + intervals[current_interval_index]
                    + (current_octave_offset * OCTAVE)
                )

                # if we are above the inclusive limit, break out of loop
                if pitch > limit:
                    break

                # if not, create note and add it to notes
                notes.append(Note(pitch, duration, dynamic))

        return cls(notes)
