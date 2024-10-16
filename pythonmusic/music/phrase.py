from functools import reduce
from typing import Any, Sequence

from .chord import Chord
from .note import Note
from .note_collection import NoteCollection
from .phrase_element import PhraseElement

__all__ = ["Phrase"]


class Phrase(NoteCollection):
    """
    Phrases group notes into connected units.

    Args:
        notes (Sequence[PhraseElement]): Notes to add. Can also be added later
    """

    __slots__ = "_notes"

    def __init__(self, notes: Sequence[PhraseElement] = []) -> None:
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
        """The phrases notes."""
        return self._notes

    @notes.setter
    def notes(self, new_value: list[PhraseElement]):
        self._notes = new_value

    def length(self) -> int:
        """
        Returns the number of elements in the phrase.

        Chords only count as one element.

        Returns:
            int: The number of elements in the phrase.
        """
        return len(self.notes)

    @property
    def duration(self) -> float:
        """
        The total unit length of the phrase.

        The returned value is equal to the sum of all note's durations.
        """
        return reduce(lambda previous, note: previous + note.duration, self.notes, 0)

    def add_chord(self, chord: Chord):
        """
        Adds the given chord to the phrase.

        Args:
            chord (Chord): The chord to add
        """
        self.notes.append(chord)

    def add_chord_by_lists(
        self, pitches: list[int], durations: list[float], dynamics: list[int]
    ):
        """
        Adds a chord constructed by the given lists.

        Args:
            pitches (list[int]): The note's pitches
            durations (list[float]): The note's durations
            dynamics (list[int]): The note's dynamics
        """
        self.add_chord(Chord.from_lists(pitches, durations, dynamics))

    def add_chords_by_lists(
        self,
        pitches: list[list[int]],
        durations: list[list[float]],
        dynamics: list[list[int]],
    ):
        """
        Adds multiple chords defined by their elements.

        Args:
            pitches (list[list[int]]): A list that contains the chord's note's
                pitchs
            durations (list[list[float]]): A list that contains the chord's note's
                durations
            dynamics (list[list[int]]): A list that contains the chord's note's
                dynamics
        """
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
        """
        Adds a rest of the given duration to the phrase.

        Args:
            duration (float): The duration of the rest to add
        """
        self.notes.append(Note.rest(duration))

    def linearise(self) -> list[tuple[float, Note]]:
        """
        Returns a list of this phrase's notes and their start times. Flattens
        chords.

        The returned start times reflect the offset in seconds of a note's start
        from the beginning of the phrase, not the part or higher.

        Because chords are a vertical structure, the resulting total duration of
        the returned notes will be higher than the original phrase. This will
        also change the melody, because chords are replaced by their linearised
        parts. Use the prepended start times to play notes individually.

        Raises:
            TypeError: If an object in the phrase is not a PhraseElement

        Returns:
            list[Note]: The linearised contents
        """

        output: list[tuple[float, Note]] = []
        start_time = 0.0

        for pe in self._notes:
            if isinstance(pe, Note):
                output.append((start_time, pe))
            elif isinstance(pe, Chord):
                output += map(lambda element: (start_time, element), pe.flatten())
            else:
                raise TypeError("Not a Phrase Element")

            start_time += pe.duration

        return output
