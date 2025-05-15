from typing import Any, Optional, Self, cast

from ..constants.dynamics import MF
from ..constants.intervals import OCTAVE
from .note import Note
from .note_collection import NoteCollection
from .phrase_element import PhraseElement

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

        length = len(self)
        if length != len(other.notes):
            return False

        for i in range(length):
            if self.notes[i] != other.notes[i]:
                return False

        return True

    def __str__(self) -> str:
        return f"Chord([{", ".join(map(lambda note: str(note), self.notes))}])"

    @classmethod
    def from_lists(
        cls,
        pitches: list[int],
        durations: list[float],
        dynamics: list[int],
        articulation: list[int] = [],
    ) -> Self:
        """
        Creates a chord by adding notes created from their individual values.

        Each list must contain at least one value. If any list has less items
        than another, its last value is repeated for all remaining notes. This
        allows, for instance, adding multiple notes with the same duration,
        without having to provide the same duration multiple times.

        Args:
            pitches (list[int]): A list of pitches
            durations (list[int]): A list of durations
            dynamics (list[int]): A list of dynamics
            articulation (list[int]): A list of articulations for the notes

        Returns:
            Chord: A chord
        """
        chord = cls()
        chord.add_notes_by_lists(pitches, durations, dynamics, articulation)

        return chord

    @property
    def notes(self) -> list[PhraseElement]:
        """
        The notes within the chord.

        Does not guarantee that the returned notes are not chords. Use
        meth:`flatten() <pythonmusic.music.Chord.flatten>` instead.
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
        limit: Optional[int] = None,
    ) -> Self:
        """Creates a chord from given intervals over a root note.

        Args:
            root (int): A root pitch
            intervals (list[int]) A list of intervals over the root note
            duration (float): The duration of the chord
            dynamic (int): The dynamic of the chord
            limit (Optional[int]): The upperlimit of the chord. If given, repeats
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

    def flatten(self) -> list[Note]:
        """
        Returns a list of all notes in the chord.

        `self.notes` returns a list of elements contained in this chord. This
        may also include other chords. This function recursively flattens
        all elements, and guarantees that the returned list only consists of
        notes.

        Raises:
            TypeError: If an object inside the chord is not a PhraseElement

        Returns:
            list[Note]: All notes in the chord
        """

        def _flatten(pe: PhraseElement) -> list[PhraseElement]:
            if isinstance(pe, Note):
                return [pe]
            if isinstance(pe, Chord):
                output = []
                for em in pe._notes:
                    output += _flatten(em)
                return output
            raise TypeError("Not a Phrase Element")

        out: list[Note] = []
        for pe in self._notes:
            out += cast(list[Note], _flatten(pe))

        return out
