import unittest

from pythonmusic.constants import *
from pythonmusic.music.chord import Chord
from pythonmusic.music.note import Note
from pythonmusic.music.part import Part
from pythonmusic.music.phrase import Phrase

PHRASE_A = Phrase([Note(1, 5.0), Note(1, 4.0), Note(1, 1.0)])
PHRASE_B = Phrase([Note(1, 10.0)])
PHRASE_C = Phrase([Note(1, 5.0), Note(1, 5.0)])


class PartTests(unittest.TestCase):
    def test_init(self):
        """Tests Part initialiser"""
        part = Part(0)
        self.assertEqual(part.title, None)
        self.assertEqual(part.instrument, ACOUSTIC_GRAND_PIANO)
        self.assertEqual(part.channel, 0)
        self.assertEqual(part.phrases_with_start_times(), [])
        self.assertEqual(part.panning, PAN_CENTER)

        phrase = Phrase([Note(1, 1), Note(2, 2)])
        part = Part(
            title="Harpsichord",
            instrument=HARPSICHORD,
            channel=5,
            phrases=[phrase],
            panning=PAN_LEFT,
        )
        self.assertEqual(part.title, "Harpsichord")
        self.assertEqual(part.instrument, HARPSICHORD)
        self.assertEqual(part.channel, 5)
        # test for add_phrases tests this more in depth
        self.assertEqual(part.phrases_with_start_times(), [(0, phrase)])
        self.assertEqual(part.panning, PAN_LEFT)

    def test_iter(self):
        chord = Chord.from_lists([A4, C4, B5], [QN], [FF])
        phrase = Phrase([Note(A4, QN), Note(C4, QN), chord])
        phrase2 = Phrase([Note(A4, QN)])

        part = Part(0, phrases=[phrase, phrase2])
        self.assertEqual(len(list(part.__iter__())), 2)

        part.add_phrase(phrase)
        self.assertEqual(len(list(part.__iter__())), 2)
        self.assertEqual(list(part.__iter__()), [phrase, phrase2])

    def test_len(self):
        """Tests Part __len__() dunder method"""
        part = Part(0, phrases=[Phrase(), Phrase()])
        self.assertEqual(part.__len__(), 2)
        part.add_phrase(Phrase())
        self.assertEqual(part.__len__(), 3)

    def test_length(self):
        """Tests Part length() method"""
        part = Part(0, phrases=[])
        self.assertEqual(part.length(), 0)
        part = Part(0, phrases=[Phrase(), Phrase(), Phrase()])
        self.assertEqual(part.length(), 3)

    def test_duration(self):
        """Tests Part duration() method"""
        part = Part(0, phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(part.duration(), 30.0)

        part = Part(0)
        part.add_phrase(PHRASE_A)  # 10
        part.add_phrase(PHRASE_B, 5.0)  # 15
        part.add_phrase(PHRASE_C)  # 25

        self.assertEqual(part.duration(), 25.0)

    def test_add_phrase(self):
        """Tests Part add_phrase() method"""
        part = Part(0)
        self.assertEqual(len(part.phrases_with_start_times()), 0)

        part.add_phrase(PHRASE_A)
        self.assertEqual(len(part.phrases_with_start_times()), 1)
        self.assertEqual(part.duration(), 10.0)

        part.add_phrase(PHRASE_B)
        self.assertEqual(len(part.phrases_with_start_times()), 2)
        self.assertEqual(part.duration(), 20.0)

        part.add_phrase(PHRASE_C, 15.0)
        self.assertEqual(len(part.phrases_with_start_times()), 3)
        self.assertEqual(part.duration(), 25.0)

    def test_add_phrases(self):
        """Test Part add_phrases() method"""
        part = Part(0)
        part.add_phrases([PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(len(part.phrases_with_start_times()), 3)
        self.assertEqual(
            part.phrases_with_start_times(),
            [(0.0, PHRASE_A), (10.0, PHRASE_B), (20.0, PHRASE_C)],
        )

        part = Part(0)
        part.add_phrases([PHRASE_A, PHRASE_B, PHRASE_C], [0.0, 1.0, 2.0])
        self.assertEqual(
            part.phrases_with_start_times(),
            [(0.0, PHRASE_A), (1.0, PHRASE_B), (2.0, PHRASE_C)],
        )
        self.assertEqual(part.duration(), 12.0)

    def test_remove_phrase(self):
        """Tests Part remove_phrase() method"""
        part = Part(0, phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        part.remove_phrase(PHRASE_B)
        self.assertEqual(
            part.phrases_with_start_times(), [(0.0, PHRASE_A), (20.0, PHRASE_C)]
        )

    def test_clear(self):
        """Tests Part clear() method"""
        part = Part(0, phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(len(part.phrases_with_start_times()), 3)
        part.clear()
        self.assertEqual(len(part.phrases_with_start_times()), 0)

    def test_linearise(self):
        """Tests Part linearisation"""
        part = Part(0, phrases=[PHRASE_A, PHRASE_B])
        self.assertEqual(
            part.linearise(),
            [
                (0.0, Note(1, 5.0)),
                (5.0, Note(1, 4.0)),
                (9.0, Note(1, 1.0)),
                (10.0, Note(1, 10.0)),
            ],
        )
