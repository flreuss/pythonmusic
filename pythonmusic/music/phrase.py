from functools import reduce
from typing import Any, Sequence

from .chord import Chord
from .note import Note
from .note_collection import NoteCollection
from .phrase_element import PhraseElement

__all__ = ["Phrase"]


class Phrase(NoteCollection):
    """Phrases group notes into connected units."""

    __slots__ = "_notes"

    def __init__(self, notes: Sequence[PhraseElement] = []) -> None:
        """
        Constructs a phrase from the given note list. Returns an empty phrase if
        no list of notes is given.

        :param list[Note] notes: A list of notes to add to the phrase
        """
        self._notes: list[PhraseElement] = []
        # Deep copies the notes given to the phrase. Modification should happen
        # inside the phrase, not the original array.
        self.add_notes(notes)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Phrase):
            return False

        length = self.length()
        if length != len(other):
            return False

        for i in range(length):
            if self.notes[i] != other.notes[i]:
                return False

        return True

    @property
    def notes(self) -> list[PhraseElement]:
        return self._notes

    @notes.setter
    def notes(self, new_value: list[PhraseElement]):
        self._notes = new_value

    def length(self) -> int:
        """
        Returns the number of elements in the phrase.

        Chords only count as one element.
        """
        return len(self.notes)

    @property
    def duration(self) -> float:
        """
        Returns the total unit length of the phrase.

        The returned value is equal to the sum of all note's durations.

        :return: The total duration of the phrase
        """
        return reduce(lambda previous, note: previous + note.duration, self.notes, 0)

    def add_chord(self, chord: Chord):
        """Adds the given chord to the phrase."""
        self.notes.append(chord)

    def add_chord_by_lists(
        self, pitches: list[int], durations: list[float], dynamics: list[int]
    ):
        """Adds a chord constructed by the given lists."""
        self.add_chord(Chord.from_lists(pitches, durations, dynamics))

    def add_chords_by_lists(
        self,
        pitches: list[list[int]],
        durations: list[list[float]],
        dynamics: list[list[int]],
    ):
        len_pitches = len(pitches)
        if len_pitches != len(durations) or len_pitches != len(dynamics):
            raise ValueError(
                f"All lists must be equal in length: pitches[{len_pitches}],\
                durations[{len(durations)}], dynamics[{len(durations)}]"
            )

        for index in range(len_pitches):
            self.add_note(
                Chord.from_lists(pitches[index], durations[index], dynamics[index])
            )

    def add_rest(self, duration: float):
        """Adds a rest of the given duration to the phrase."""
        self.notes.append(Note.rest(duration))

    def linearise(self) -> list[Note]:
        """
        Returns a list of this phrase's notes, where chords are flattened.

        Because chords are a vertical structure, the resulting total duration of
        the returned notes will be higher than the original phrase. This will
        also change the melody, because chords are replaced by their linearised
        parts.
        """

        def _flatten(input: PhraseElement) -> list[Note]:
            if isinstance(input, Note):
                return [input]
            elif isinstance(input, Chord):
                output = []
                for pe in input.notes:
                    output += _flatten(pe)
                return output
            return []

        output = []
        for pe in self.notes:
            output += _flatten(pe)
        return output
