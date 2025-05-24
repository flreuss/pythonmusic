from typing import Iterator, Optional

from pythonmusic.constants.instruments import ACOUSTIC_GRAND_PIANO
from pythonmusic.constants.panning import PAN_CENTER
from pythonmusic.util import contains_identity

from .note import Note
from .phrase import Phrase

__all__ = ["Part"]


class Part:
    """
    A part represents an instrument and consists of phrases.

    Args:
        channel (int): A zero-indexed channel
        title (Optional[str]): A title for the part. Defaults to `None`
        instrument (int): An instrument for the part
        phrases (list[Phrase]): A list of phrases to add to the part. Phrases
            can also be added later
        panning (int): Panning in range from 0 to 127. Defaults to centre, 64
    """

    def __init__(
        self,
        channel: int,
        title: Optional[str] = None,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        phrases: list[Phrase] = [],
        panning: int = PAN_CENTER,
    ) -> None:
        self.title: Optional[str] = title
        self.instrument: int = instrument
        self.channel: int = channel
        self._elements: list[tuple[float, Phrase]] = []
        self.panning: int = panning

        self.add_phrases(phrases, None)

    def __iter__(self) -> Iterator[Phrase]:
        """
        Returns an iterator over this parts phrases.

        Identical phrases that have been added multiple times are only yielded
        once. Use `Part().phrases()` or `Part().phrases_with_start_times() for
        a complete list.
        """
        visited: list[Phrase] = []

        for _, phrase in self._elements:
            if contains_identity(visited, phrase):
                continue

            visited.append(phrase)
            yield phrase

    def phrases(self) -> list[Phrase]:
        """
        Returns a list over this part's phrases.

        The part stores phrases as tuples of a start time and a phrase. If you
        need both, use `phrases_with_start_times()` instead.

        Keep in mind that phrases may occur multiple times in the same part.

        Returns:
            list[Phrase]: A list of this part's phrases
        """
        return list(map(lambda element: element[1], self._elements))

    def phrases_with_start_times(self) -> list[tuple[float, Phrase]]:
        """
        Returns a list of this part's phrases with their start times.

        Keep in mind that phrases may occur multiple times in the same part.

        Returns:
            list[tuple[float, Phrase]]: A list of tuples representing this
                part's phrases and their start times (start_time, phrase)
        """
        return self._elements

    def __len__(self) -> int:
        return self._elements.__len__()

    def duration(self) -> float:
        """
        Returns the total unit length of the phrase.

        The returned value is equal to the end time of the last phrase to be
        played. Returns `0` if no phrases are added to the part.

        Returns:
            The total duration of this phrase
        """

        # default to 0, if empty. Will also prevent exception below for max(None)
        if self._elements.__len__() == 0:
            return 0

        # iterates over all phrases and calculates their end time by adding
        # their start time to their duration. The maximum value of that is the
        # duration of the phrase aka. When the last phrase ends
        return max(
            map(
                lambda item: item[0] + item[1].duration,
                self._elements,
            )
        )

    def add_phrase(self, phrase: Phrase, start_time: Optional[float] = None):
        """
        Adds the given phrase to the part.

        Optionally, you can provide a start_time at which the phrase should
        begin. If none if provided, the phrase will be appended to the end of
        the part.

        Args:
            phrase (Phrase): A phrase to add
            start_time (Optional[float]): Time at which the phrase should start.
                Defaults to the end of the part, so the phrase is appended to
                the end and played after the last phrase ends
        """

        # calculate start time, if none was given / append to end
        start_time = start_time if start_time is not None else self.duration()
        self._elements.append((start_time, phrase))

    def add_phrases(
        self,
        phrases: list[Phrase],
        start_times: Optional[list[Optional[float]]] = None,
    ):
        """
        Adds the given phrases to the part.

        Optionally, you can provide a list of start times. If you do provide
        start times the length of that list must match the number of phrases to
        add. However, to explicitly not assign a start time to a phrase, set its
        index in `start_times` to `None`.

        Example:
            In the example below, `phrase_b` will be appended to the end the part.
              Phrases with an explicit start time are added first, so `phrase_b`
              will sound after `phrase_a` and `phrase_c`.

                >>> phrases = [phrase_a, phrase_b, phrase_c]
                >>> start_times = [3.5, None, 5.5]
                >>> my_part.add_phrases(phrases, start_times)

        Args:
            phrases (list[Phrase]): The phrases to add
            start_time (Optional[list[Optional[float]]]): The phrases' start times
        """

        # check if start_times was provided
        if start_times is None:
            # if not generate list of None with length of len(phrases)
            # this setup is needed to satisfy the type checker
            NONE_ELEMENT: list[Optional[float]] = [None]
            start_times = NONE_ELEMENT * len(phrases)
        else:
            # otherwise, check that length is equal
            if len(phrases) != len(start_times):
                raise ValueError(
                    f"All lists must be equal in length: phrases[{len(phrases)}], start_times[{len(start_times)}]"
                )

        # packs elements in to tuples
        elements = list(zip(start_times, phrases))
        non_st_elements: list[Phrase] = []  # st: start_time

        for element in elements:
            # splitting here allows the type checker to guarantee that st is not `None`
            (start_time, phrase) = element
            if start_time is None:
                non_st_elements.append(phrase)
                continue

            self._elements.append((start_time, phrase))

        # iterates left over phrases and adds them to the end; updates end
        start_time = self.duration()
        for phrase in non_st_elements:
            self._elements.append((start_time, phrase))
            start_time += phrase.duration

    def shift_start_time(self, delta: float):
        """
        Changes the start time of the phrase by shifting the start times of
        all its phrases.

        While `delta` can be negative to decrease the start offset, phrases
        cannot start at a value below ``0``.

        Args:
            delta(float): Change in start time
        """

        done: list[Phrase] = []

        for index, (start_time, phrase) in enumerate(self._elements):
            if phrase in done:
                continue
            done.append(phrase)

            self._elements[index] = (max(0, start_time + delta), phrase)

    def remove_phrase(self, phrase: Phrase):
        """
        Removes the given phrase from the part.

        The phrase to be removed is compared by identity, not contents, so to
        remove a phrase that same object must be provided here.

        Raises:
            ValueError: If the given phrase does not exist in the part

        Args:
            phrase (Phrases): The phrase to remove
        """

        for index, element in enumerate(self._elements):
            if phrase is element[1]:
                self._elements.pop(index)
                return
        raise ValueError("The given phrase is not in part")

    def clear(self):
        """Removes all phrases from the part."""
        self._elements = []

    def linearise(self) -> list[tuple[float, Note]]:
        """
        Returns a list of all notes in the part with their start times.

        A part may consist of multiple phrases that all start at different times.
        Use this method to retrieve a list of all notes independent of their
        phrases, with their respective start times in seconds from the beginning
        of playback.

        This method is useful in scenarios where you need the notes of a part,
        but don't care about phrase boundaries.

        .. code-block:: python

            part = Part(0, "some part")

            # add phrases as needed
            ...

            # iterate over all notes in part
            for note_start_time, note in part.linearise()):
                print(f"Note with pitch {note.pitch} starts at {note_start_time}")


        .. note::
            The returned list is not sorted, because it depends on the order in
            which phrases where added to the part. Sort as needed:

            .. code-block:: python

                for note_start_time, note in sorted(part.linearise(), key=lambda tupl: tupl[0]):
                    print(f"Note with pitch {note.pitch} starts at {note_start_time}")

        Returns:
            list[tuple[float, Note]]: All notes contained in the phrase with
                their start_time attached
        """
        notes: list[tuple[float, Note]] = []

        for phrase_start_time, phrase in self.phrases_with_start_times():
            for note_start_time, note in phrase.linearise():
                notes.append((phrase_start_time + note_start_time, note))

        return notes
