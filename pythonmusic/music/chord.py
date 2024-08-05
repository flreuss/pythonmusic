from typing import cast as _cast, Any

from .note import Note
from .phrase_element import PhraseElement
from .note_collection import NoteCollection
from ..constants.dynamics import MF as _MF
from ..constants.intervals import OCTAVE as _OCTAVE


class Chord(PhraseElement, NoteCollection):
    """A type that groups multiple notes together."""

    __slots__ = "_notes"

    def __init__(self, notes: list[Note] = []) -> None:
        self._notes = []
        self.add_notes(_cast(list[PhraseElement], notes))

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
        """Returns the number of notes in the chord."""
        return len(self.notes)

    @property
    def notes(self) -> list[PhraseElement]:
        return self._notes

    @notes.setter
    def notes(self, new_value: list[PhraseElement]):
        self._notes = new_value

    @property
    def duration(self) -> float:
        """Returns the duration of the chord."""
        return self.max_duration() or 0.0

    def is_note(self) -> bool:
        return False

    def is_chord(self) -> bool:
        return True

    @staticmethod
    def from_root(
        root: int,
        intervals: list[int],
        duration: float,
        dynamic: int = _MF,
        limit: int | None = None,
    ) -> "Chord":
        """Creates a chord from given intervals over a root note.

        :param root: A root pitch.
        :param intervals: A list of intervals over the root note
        :duration: The duration of the chord
        :dynamic: The chord's dynamic, defaults to `MF`
        :limit: Optional, the upper pitch limit until which the chord will be
            constructed. If `None`, the given intervald will only be added once.

        :return: The constructed chord.
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
                    + (current_octave_offset * _OCTAVE)
                )

                # if we are above the inclusive limit, break out of loop
                if pitch > limit:
                    break

                # if not, create note and add it to notes
                notes.append(Note(pitch, duration, dynamic))

        return Chord(notes)
