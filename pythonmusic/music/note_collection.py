from abc import ABC, abstractmethod
from functools import reduce
from typing import Iterator, Optional, Sequence, cast

from .note import Note
from .phrase_element import PhraseElement

__all__ = ["NoteCollection"]


class NoteCollection(ABC):
    """
    An abstract class that defines methods for chords and phrases.
    """

    def __iter__(self) -> Iterator[PhraseElement]:
        for note in self.notes:
            yield note

    def __getitem__(self, index: int) -> PhraseElement:
        return self.notes[index]

    @property
    @abstractmethod
    def notes(self) -> list[PhraseElement]:
        """The notes contained in this collection."""
        pass

    @notes.setter
    @abstractmethod
    def notes(self, new_value: list[PhraseElement]):
        pass

    @staticmethod
    def _flatten(elements: list[PhraseElement]) -> list[Note]:
        """
        Flattens the given list of phrase elements by unpacking chords.
        """

        def inner(elements: list[PhraseElement]) -> list[PhraseElement]:
            output: list[PhraseElement] = []
            for element in elements:
                if element.is_note():
                    output.append(element)
                    continue
                if element.is_chord():
                    # Below, typechecking is disabled. This avoids a circular
                    # import issue where Chord needs to imported as well.
                    # TYPE: element is guaranteed to be Chord
                    output.extend(inner(element.notes))  # type: ignore

                raise TypeError("Invalid PhraseElement")

            return output

        return cast(list[Note], inner(elements))

    def __len__(self) -> int:
        """Returns the number of notes in this collection."""
        return self.notes.__len__()

    # due to chord needing to conform both to NoteColelction
    @property
    @abstractmethod
    def duration(self) -> float:
        """The duration of this collection."""
        pass

    def add_note(self, note: PhraseElement):
        """
        Adds the given note to the collection.

        Args:
            note (PhraseElement): A phrase element (note, chord) to add
        """
        self.notes.append(note)

    def add_notes(self, notes: Sequence[PhraseElement]):
        """
        Adds the given notes to the collection.

        Args:
            note (Sequence[PhraseElement]): Phrase elements to add
        """
        self.notes.extend(notes)

    def add_notes_by_lists(
        self,
        pitches: list[int],
        durations: list[float],
        dynamics: list[int],
        articulation: list[int] = [],
    ):
        """
        Adds notes defined by their parts.

        Provide lists of pitches, durations, and dynamics that describe the notes
        to add.

        Each list must contain at least one value. If any list has less items
        than another, its last value is repeated for all remaining notes. This
        allows, for instance, adding multiple notes with the same duration,
        without having to provide the same duration multiple times.

        Raises:
            ValueError: If any list is empty

        Args:
            pitches (list[int]): A list of pitches
            durations (list[float]): A list of durations
            dynamics (list[int]): A list of dynamics
            articulation(list[int]): A list of articulations for the notes
        """
        # no idea if len is trivial in python
        len_pitches = len(pitches)
        len_durations = len(durations)
        len_dynamics = len(dynamics)

        if len_pitches == 0:
            raise ValueError("At least one pitch must be given")

        if len_durations == 0:
            raise ValueError("At least one duration must be given")

        if len_dynamics == 0:
            raise ValueError("At least one dynamic must be given")

        max_length = max(len_pitches, len_durations, len_dynamics)

        # create notes form SoA
        self.add_notes(
            list(
                map(
                    lambda i: Note(
                        # use i, or clip to last index (repeat last)
                        pitches[min(i, len_pitches - 1)],
                        durations[min(i, len_durations - 1)],
                        dynamics[min(i, len_dynamics - 1)],
                        articulation,
                    ),
                    range(max_length),
                )
            )
        )

    def remove_note(self, index: int) -> PhraseElement:
        """
        Removes the note at the given index and returns it.

        Notes are ordered how they are added. The first note that was added to
        a note collection is at index `0`, the second at index `1`, ...

        Raises:
            IndexError: If given index is out of bounds

        Args:
            index (int): The index of the phrase element to be removed

        Returns:
            PhraseElement: The removed phrase element
        """

        return self.notes.pop(index)

    def clear(self):
        """Removes all notes from the collection."""
        self.notes.clear()

    def min_pitch(self) -> Optional[int]:
        """
        Returns the smallest pitch in the collection or `None` if empty.
        Ignores rests.

        Returns:
            Optional[int]: The minimum pitch or `None` if collection is empty
        """
        if len(self.notes) == 0:
            return None

        INVALID_PITCH = 1000
        notes = self._flatten(self.notes)
        return reduce(
            lambda current, next: (
                min(current, next.pitch) if not next.is_rest() else current
            ),
            notes,
            INVALID_PITCH,
        )

    def max_pitch(self) -> Optional[int]:
        """
        Returns the highest pitch in the collection or `None` if empty.
        Ignores rests.

        Returns:
            Optional[int]: The highest pitch in the collection of `None` if empty
        """
        if len(self.notes) == 0:
            return None
        notes = self._flatten(self.notes)
        return reduce(
            lambda current, next: (
                max(current, next.pitch) if not next.is_rest() else current
            ),
            notes,
            0,
        )

    def min_duration(self) -> Optional[float]:
        """
        Returns the smallest duration in the collection or `None` if empty.

        Returns:
            Optional[float]: The smallest duration in the collection of `None` if empty
        """
        return (
            min(map(lambda note: note.duration, self.notes))
            if len(self.notes) != 0
            else None
        )

    def max_duration(self) -> Optional[float]:
        """
        Returns the highest duration in the collection or `None` if empty.

        Returns:
            Optional[float]: The highest duration in the collection of `None` if empty
        """
        return (
            max(map(lambda note: note.duration, self.notes))
            if len(self.notes) != 0
            else None
        )

    def min_dynamic(self) -> Optional[int]:
        """
        Returns the smallest dynamic in the collection or `None` if empty.
        Ignores rests.

        Returns:
            Optional[int]: The smallest dynamic in the collection of `None` if empty
        """
        if len(self.notes) == 0:
            return None

        INVALID_DYNAMIC = 200  # a value above valid dynamic range
        notes = self._flatten(self.notes)
        return reduce(
            lambda current, next: (
                min(current, next.dynamic) if not next.is_rest() else current
            ),
            notes,
            INVALID_DYNAMIC,
        )

    def max_dynamic(self) -> Optional[int]:
        """
        Returns the highest dynamic in the collection or `None` if empty.
        Ignores rests.

        Returns:
            Optional[int]: The highest dynamic in the collection of `None` if empty
        """
        if len(self.notes) == 0:
            return None

        notes = self._flatten(self.notes)
        return reduce(
            lambda current, next: (
                max(current, next.dynamic) if not next.is_rest() else current
            ),
            notes,
            0,
        )
