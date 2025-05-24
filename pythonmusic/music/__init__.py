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
    "legato",
    "legato_l",
]


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
