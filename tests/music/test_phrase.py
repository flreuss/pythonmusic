import unittest
from pythonmusic.music.note import Note
from pythonmusic.music.phrase import Phrase
from pythonmusic.constants.pitches import *
from pythonmusic.constants.durations import *

NOTES = [
    Note(C3, QN),
    Note(E3, QN),
    Note(G4, DEN),
    Note(G4, SN),
    Note(C5, DEN),
    Note(C5, SN),
    # /
    Note(D5, DQN),
    Note.rest(EN),
    Note(D5, EN),
    Note(B4, EN),
    Note(G4, EN),
    Note(F4, SN),
    Note(F4, SN),
    # /
    Note(E4, QN),
    Note(E4, QN),
    Note(E4, EN),
    Note(GS4, EN),
    Note(B4, EN),
    Note(E4, SN),
    Note(E4, SN),
    # /
    Note(C5, DEN),
    Note(C5, SN),
    Note(C5, HN),
    Note(C5, EN),
    Note(C5, EN),
    # /
    Note(BF4, DEN),
    Note(BF4, SN),
    Note(BF4, EN),
    Note(C5, EN),
    Note(A4, HN),
]


class PhraseTests(unittest.TestCase):
    def test_init(self):
        """Tests Phrase.__init__"""
        self.assertFalse(True)
