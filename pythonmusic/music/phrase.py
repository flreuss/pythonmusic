from functools import reduce as _reduce
from .note import Note


class Phrase:
    """Phrases group notes into connected units."""

    __slots__ = "notes"

    def __init__(self, notes: list[Note] = []) -> None:
        """
        Constructs a phrase from the given note list. Returns an empty phrase if
        no list of notes is given.

        :param list[Note] notes: A list of notes to add to the phrase
        """
        self.notes: list[Note] = []
        # Deep copies the notes given to the phrase. Modification should happen
        # inside the phrase, not the original array.
        self.add_notes(notes)

    def __len__(self) -> int:
        return self.notes.__len__()

    def __str__(self) -> str:
        notes_str = ""
        note_end_index = len(self.notes) - 1
        for index, note in enumerate(self.notes):
            notes_str += str(note)
            if not index == note_end_index:
                notes_str += ", "

        return f"Phrase({notes_str})"

    def length(self) -> int:
        """Returns the number of notes in the phrase."""
        return len(self.notes)

    def duration(self) -> float:
        """
        Returns the total unit length of the phrase.

        The returned value is equal to the sum of all note's durations.

        :return: The total duration of the phrase
        """
        return _reduce(
            lambda previous, note: previous + note.duration, self.notes, 0
        )

    def add_note(self, note: Note):
        """Adds the given note to the phrase."""
        self.notes.append(note)

    def add_notes(self, notes: list[Note]):
        """Adds the given notes to the phrase."""
        self.notes += notes

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
                f"All lists must be equal in length: pitches[{len_pitches}], durations[{len(durations)}], dynamics[{len(durations)}]"
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

    def remove_note(self, index: int) -> Note:
        """
        Removes the note at the given index and optionally returns it.

        :param int index: The index of the note to be removed
        :return: The removed note
        :raises IndexError: If given index is outsides bounds
        """

        return self.notes.pop(index)

    def clear(self):
        """Removes all notes from the phrase."""
        self.notes = []

    def min_pitch(self) -> int | None:
        """
        Returns the smallest pitch in the phrase or `None` if empty.
        Ignores rests.

        :return: The smallest pitch in the phrase of `None` if empty
        """
        INVALID_PITCH = 1000
        return (
            _reduce(
                lambda current, next: (
                    min(current, next.pitch) if not next.is_rest() else current
                ),
                self.notes,
                INVALID_PITCH,
            )
            if len(self.notes) != 0
            else None
        )

    def max_pitch(self) -> int | None:
        """
        Returns the highest pitch in the phrase or `None` if empty.
        Ignores rests.

        :return: The highest pitch in the phrase of `None` if empty
        """
        return (
            _reduce(
                lambda current, next: (
                    max(current, next.pitch) if not next.is_rest() else current
                ),
                self.notes,
                0,
            )
            if len(self.notes) != 0
            else None
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
        INVALID_DYNAMIC = 200  # a value above valid dynamic range
        return (
            _reduce(
                lambda current, next: (
                    min(current, next.dynamic)
                    if not next.is_rest()
                    else current
                ),
                self.notes,
                INVALID_DYNAMIC,
            )
            if len(self.notes) != 0
            else None
        )

    def max_dynamic(self) -> int | None:
        """
        Returns the highest dynamic in the phrase or `None` if empty.
        Ignores rests.

        :return: The highest dynamic in the phrase of `None` if empty
        """
        return (
            _reduce(
                lambda current, next: (
                    max(current, next.dynamic)
                    if not next.is_rest()
                    else current
                ),
                self.notes,
                0,
            )
            if len(self.notes) != 0
            else None
        )
