from copy import deepcopy
from itertools import chain
from typing import Sequence

from pythonmusic.constants.intervals import OCTAVE
from pythonmusic.music import Chord, Note, Phrase, PhraseElement

__all__ = [
    "concat_phrases",
    "repeat_phrase",
    "pitch",
    "pitch_phrase",
    "octave",
    "octave_phrase",
]


def concat_phrases(phrases: Sequence[Phrase]) -> Phrase:
    """
    Chains the given phrases into one.

    The input is copied and is not mutated.

    Args:
        phrases(Sequence[Phrase]): A list of phrases

    Returns:
        Phrase: Phrase containing all given phrases
    """
    return Phrase(
        list(chain.from_iterable(deepcopy(phrase.notes) for phrase in phrases))
    )


def repeat_phrase(phrase: Phrase, n: int) -> Phrase:
    """
    Creates a new phrase by repeating the given phrase `n` times.

    Args:
        phrase(Phrase): A phrase
        n(int): How often to repeat the phrase

    Returns:
        Phrase: A new phrase
    """
    return concat_phrases([phrase] * n)


def pitch(elements: Sequence[PhraseElement], interval: int) -> list[PhraseElement]:
    """
    Pitches all given notes or chords by the specified interval.

    Args:
        elements(Sequence[PhraseElement]): A list of notes or chords
        interval(int): The interval to pitch by in semitones

    Returns:
        list[PhraseElement]: A list containing the pitched notes
    """

    def _pitch(element: PhraseElement, interval: int) -> PhraseElement:
        if isinstance(element, Note):
            note: Note = deepcopy(element)
            if not note.is_rest():
                note.pitch += interval
            return note

        if isinstance(element, Chord):
            chord: Chord = element
            out: Chord = Chord()
            for index in range(len(chord.notes)):
                out.add_note(_pitch(chord.notes[index], interval))

            return out

        raise TypeError(f"Given element is not a Note or Chord, but {type(element)}")

    return list(map(lambda element: _pitch(element, interval), elements))


def pitch_phrase(phrase: Phrase, interval: int) -> Phrase:
    """
    Pitches the given phrase by an interval.

    Returns a new phrase. The original phrase is not mutated.

    Args:
        phrase(Phrase): A phrase
        interval(int): An inteval to pich by

    Returns:
        Phrase: A pitched phrase
    """

    return Phrase(pitch(phrase.notes, interval))


def octave(elements: Sequence[PhraseElement], n: int = 1) -> list[PhraseElement]:
    """
    Pitches all given notes or chords by `n` octaves.

    Args:
        elements(Sequence[PhraseElement]): A list of notes or chords
        n(int): Number of octaves to pitch by. Set negative to pitch down

    Returns:
        list[PhraseElement]: A list containing the pitched notes
    """

    return pitch(elements, OCTAVE * n)


def octave_phrase(phrase: Phrase, n: int = 1) -> Phrase:
    """
    Pitches a phrase up by `n` octaves.

    Args:
        phrase(Phrase): A phrase to pitch
        n(int): Number of octaves to pitch by. Set negative to pitch down

    Returns:
        Phrase: The pitched phrase
    """

    return Phrase(octave(phrase.notes, n))
