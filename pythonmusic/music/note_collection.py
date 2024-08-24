from .phrase_element import PhraseElement
from .note import Note

from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod
from functools import reduce as _reduce
from typing import Sequence, cast as _cast


class NoteCollection(_ABC):
    @property
    @_abstractmethod
    def notes(self) -> list[PhraseElement]:
        pass

    @notes.setter
    @_abstractmethod
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

        return _cast(list[Note], inner(elements))

    def __len__(self) -> int:
        """Returns the number of notes in this colleciton."""
        return self.notes.__len__()

    # due to chord needing to conform both to NoteColelction
    @property
    @_abstractmethod
    def duration(self) -> float:
        pass

    def add_note(self, note: Note):
        """Adds the given note to the collection."""
        self.notes.append(note)

    def add_notes(self, notes: Sequence[PhraseElement]):
        """Adds the given notes to the collection."""
        self.notes.extend(notes)

    def add_notes_by_lists(
        self,
        pitches: list[int],
        durations: list[float],
        dynamics: list[int],
    ) -> None:
        """
        Adds notes defined by their parts to the phrase.

        Provide lists of pitches, durations, and dynamics that describe the notes
        to add.

        The lists must be parallel and are expected to be equal in length, where
        one note represents one entry from `pitches`, `durations`, and
        `dynamics`, respectively.

        ```python
        for index in range(0, len(pitches)):
            note = Note(pitches[i], durations[i], dynamics[i])
            notes.append(note)
        ```

        :param list[int] pitches: A list of pitches
        :param list[float] durations: A list of durations
        :param list[int] dynamics: A list of dynamics
        :raises ValueError: if arrays are not the same length
        """

        # assert that all lists are parallel
        len_pitches = len(pitches)
        if len(durations) != len_pitches or len(dynamics) != len_pitches:
            raise ValueError(
                f"All lists must be equal in length: pitches[{len_pitches}],\
                durations[{len(durations)}], dynamics[{len(durations)}]"
            )

        # create notes form SoA
        self.add_notes(
            list(
                map(
                    lambda i: Note(pitches[i], durations[i], dynamics[i]),
                    range(0, len(pitches)),
                )
            )
        )

    def remove_note(self, index: int) -> PhraseElement:
        """
        Removes the note at the given index and optionally returns it.

        :param int index: The index of the note to be removed
        :return: The removed note
        :raises IndexError: If given index is outsides bounds
        """

        return self.notes.pop(index)

    def clear(self):
        """Removes all notes from the phrase."""
        self.notes.clear()

    def min_pitch(self) -> int | None:
        """
        Returns the smallest pitch in the phrase or `None` if empty.
        Ignores rests.

        :return: The smallest pitch in the phrase of `None` if empty
        """
        if len(self.notes) == 0:
            return None

        INVALID_PITCH = 1000
        notes = self._flatten(self.notes)
        return _reduce(
            lambda current, next: (
                min(current, next.pitch) if not next.is_rest() else current
            ),
            notes,
            INVALID_PITCH,
        )

    def max_pitch(self) -> int | None:
        """
        Returns the highest pitch in the phrase or `None` if empty.
        Ignores rests.

        :return: The highest pitch in the phrase of `None` if empty
        """
        if len(self.notes) == 0:
            return None
        notes = self._flatten(self.notes)
        return _reduce(
            lambda current, next: (
                max(current, next.pitch) if not next.is_rest() else current
            ),
            notes,
            0,
        )

    def min_duration(self) -> float | None:
        """
        Returns the smallest duration in the phrase or `None` if empty.

        :return: The smallest duration in the phrase of `None` if empty
        """
        return (
            min(map(lambda note: note.duration, self.notes))
            if len(self.notes) != 0
            else None
        )

    def max_duration(self) -> float | None:
        """
        Returns the highest duration in the phrase or `None` if empty.

        :return: The highest duration in the phrase of `None` if empty
        """
        return (
            max(map(lambda note: note.duration, self.notes))
            if len(self.notes) != 0
            else None
        )

    def min_dynamic(self) -> int | None:
        """
        Returns the smallest dynamic in the phrase or `None` if empty.
        Ignores rests.

        :return: The smallest dynamic in the phrase of `None` if empty
        """
        if len(self.notes) == 0:
            return None

        INVALID_DYNAMIC = 200  # a value above valid dynamic range
        notes = self._flatten(self.notes)
        return _reduce(
            lambda current, next: (
                min(current, next.dynamic) if not next.is_rest() else current
            ),
            notes,
            INVALID_DYNAMIC,
        )

    def max_dynamic(self) -> int | None:
        """
        Returns the highest dynamic in the phrase or `None` if empty.
        Ignores rests.

        :return: The highest dynamic in the phrase of `None` if empty
        """
        if len(self.notes) == 0:
            return None

        notes = self._flatten(self.notes)
        return _reduce(
            lambda current, next: (
                max(current, next.dynamic) if not next.is_rest() else current
            ),
            notes,
            0,
        )
