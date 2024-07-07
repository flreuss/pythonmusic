from functools import reduce as _reduce
from .note import Note
from ..constants.dynamics import MF as _MF
from ..constants.intervals import OCTAVE as _OCTAVE


class Chord:
    """A type that groups multiple notes together."""

    __slots__ = "notes"

    def __init__(self, notes: list[Note] = []) -> None:
        self.notes = []
        self.add_notes(notes)

    def __len__(self) -> int:
        return self.notes.__len__()

    def length(self) -> int:
        """Returns the number of notes in the chord."""
        return len(self.notes)

    def duration(self) -> float:
        """Returns the duration of the chord."""
        wev

    def add_note(self, note: Note):
        """Adds the given note to the chord."""
        self.notes.append(note)

    def add_notes(self, notes: list[Note]):
        """Adds the given notes to the chord."""
        self.notes += notes

    def remove_note(self, index: int):
        """Removes the note at the given index."""
        self.notes.pop(index)

    def clear(self):
        """Removes all notes from the chord."""
        self.notes = []

    def min_pitch(self) -> int | None:
        """Returns the lowest pitch in the chord or `None` if empty.

        Assumes that no rests are in the chord.

        :return: The lowest pitch in the chord or `None` if empty.
        """
        return (
            _reduce(lambda current, next: min(current, next.pitch), self.notes)
            if len(self.notes) != 0
            else None
        )

    def max_pitch(self) -> int | None:
        """Returns the highest pitch in the chord or `None` if empty.

        :return:The highest pitch in the chord or `None` if empty.
        """
        return (
            _reduce(lambda current, next: max(current, next.pitch), self.notes)
            if len(self.notes) != 0
            else None
        )

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
            notes = [
                Note(root + interval, duration, dynamic)
                for interval in intervals
            ]

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
