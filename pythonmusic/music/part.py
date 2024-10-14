from .phrase import Phrase
from .note import Note
from pythonmusic.constants.panning import PAN_CENTER
from pythonmusic.constants.instruments import ACOUSTIC_GRAND_PIANO

__all__ = ["Part"]


class Part:
    """
    A part represents an instrument and consists of phrases.

    Args:
        title (str | None): A title for the part. Defaults to `None`
        instrument (int): An instrument for the part
        phrases (list[Phrase]): A list of phrases to add to the part. Phrases
            can be added later
        channel (int): A zero-indexed channel
        panning (int): Panning in range from 0 to 127. Defaults to centre, 64
    """

    def __init__(
        self,
        title: str | None = None,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        phrases: list[Phrase] = [],
        channel: int = 0,
        panning: int = PAN_CENTER,
    ) -> None:
        self.title: str | None = title
        self.instrument: int = instrument
        self.channel: int = channel
        self.phrases: list[tuple[float, Phrase]] = []
        self.panning: int = panning

        self.add_phrases(phrases, None)

    def __len__(self) -> int:
        return self.phrases.__len__()

    def length(self) -> int:
        """Returns the number of phrases in the part."""
        return len(self)

    def duration(self) -> float:
        """
        Returns the total unit length of the phrase.

        The returned value is equal to the end time of the last phrase to be
        played. Returns `0` if no phrases are added to the part.

        Returns:
            The total duration of this phrase
        """

        # default to 0, if empty. Will also prevent exception below for max(None)
        if self.phrases.__len__() == 0:
            return 0

        # iterates over all phrases and calculates their end time by adding
        # their start time to their duration. The maximum value of that is the
        # duration of the phrase aka. When the last phrase ends
        return max(
            map(
                lambda item: item[0] + item[1].duration,
                self.phrases,
            )
        )

    def add_phrase(self, phrase: Phrase, start_time: float | None = None):
        """
        Adds the given phrase to the part.

        Optionally, you can provide a start_time at which the phrase should
        begin. If none if provided, the phrase will be appended to the end of
        the part.

        Args:
            phrase (Phrase): A phrase to add
            start_time (float | None): Time at which the phrase should start.
                Defaults to the end of the part, so the phrase is appended to
                the end and played after the last phrase ends
        """

        # calculate start time, if none was given / append to end
        start_time = start_time if start_time is not None else self.duration()
        self.phrases.append((start_time, phrase))

    def add_phrases(
        self,
        phrases: list[Phrase],
        start_times: list[float | None] | None = None,
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
            start_time (list[float | None]): The phrases' start times
        """

        # check if start_times was provided
        if start_times is None:
            # if not generate list of None with length of len(phrases)
            # this setup is needed to satisfy the type checker
            NONE_ELEMENT: list[float | None] = [None]
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

            self.phrases.append((start_time, phrase))

        # iterates left over phrases and adds them to the end; updates end
        start_time = self.duration()
        for phrase in non_st_elements:
            self.phrases.append((start_time, phrase))
            start_time += phrase.duration

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

        for index, element in enumerate(self.phrases):
            if phrase is element[1]:
                self.phrases.pop(index)
                return
        raise ValueError("The given phrase is not in part")

    def clear(self):
        """Removes all phrases from the part."""
        self.phrases = []

    def linearise(self) -> list[tuple[float, Note]]:
        """
        Returns a list of this part's notes flattened.

        Use this function to retrieve all notes contained in this part.
        Because Phrases are not necessarily contiguous, each note is also
        prefixed by its start time.

        The returned list is not sorted and may not be in order of start times.

        Returns:
            list[tuple[float, Note]]: All notes contained in the phrase with
                their start_time attached
        """
        notes: list[tuple[float, Note]] = []

        # for start_time, phrase in self.phrases:
        #     for note in phrase.linearise()

        return notes
