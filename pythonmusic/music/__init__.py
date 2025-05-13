from pythonmusic.constants.instruments import INSTRUMENT_INDEX
from pythonmusic.util import instrument_get_patch_bank

from .chord import Chord
from .note import Note
from .note_collection import NoteCollection
from .part import Part
from .phrase import Phrase
from .phrase_element import PhraseElement
from .score import Score

__all__ = [
    "NoteCollection",
    "PhraseElement",
    "Note",
    "Chord",
    "Phrase",
    "Part",
    "Score",
    # functions
    "sharp",
    "flat",
    "dotted",
    "legato",
]


def sharp(pitch: int) -> int:
    """
    Returns the given pitch raised by one.

    .. note:: This is equivalent to ``pitch + 1``.

    Args:
        pitch (int): The base pitch

    Returns:
        int: Increased pitch
    """
    return pitch + 1


def flat(pitch: int) -> int:
    """
    Returns the given pitch lowered by one.

    Args:
        pitch (int): The base pitch

    Returns:
        int: Decreased pitch

    .. note:: This is equivalent to ``pitch - 1``."""
    return pitch - 1


def dotted(duration: float, dots: int = 1) -> float:
    """
    Calculates the length of a dotted note.

    Args:
        duration(float): The base note's duration
        dots(int): The number of dots to apply

    Returns:
        float: The new duration
    """
    if dots < 1:
        return duration
    return duration * (2 - (0.5**dots))


def legato_l(notes: list[Note]) -> list[Note]:
    """
    Adds legato to a list of notes.

    Args:
        notes(list[Note]): A list of notes

    Returns:
        list[Note]: Given notes with legato applied
    """
    return list(map(lambda note: note.with_legato(), notes))


def legato(*notes: Note) -> list[Note]:
    """
    Adds legato to all given notes.

    Args:
        *notes(note): Any number of notes

    Returns:
        list[Note]: Given notes with legato applied
    """
    return legato_l(list(notes))


def instrument_get_name(instrument: int) -> str:
    """
    Returns the name for the given instrument

    Args:
        instrument(int): One of this library's instruments

    Returns:
        str: The name of the instrument
    """
    return INSTRUMENT_INDEX[instrument]
