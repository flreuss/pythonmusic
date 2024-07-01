import unittest
from pythonmusic.music.note import Note
from pythonmusic.music.phrase import Phrase
from pythonmusic.music.part import Part
from pythonmusic.constants import *


PHRASE_A = Phrase([Note(1, 5.0), Note(1, 4.0), Note(1, 1.0)])
PHRASE_B = Phrase([Note(1, 10.0)])
PHRASE_C = Phrase([Note(1, 5.0), Note(1, 5.0)])


class PartTests(unittest.TestCase):
    def test_init(self):
        """Tests Part initialiser"""
        part = Part()
        self.assertEqual(part.title, None)
        self.assertEqual(part.instrument, ACOUSTIC_GRAND_PIANO)
        self.assertEqual(part.channel, 1)
        self.assertEqual(part.phrases, [])
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
        self.assertEqual(part.phrases, [(0, phrase)])
        self.assertEqual(part.panning, PAN_LEFT)

    def test_len(self):
        """Tests Part __len__() dunder method"""
        part = Part(phrases=[Phrase(), Phrase()])
        self.assertEqual(part.__len__(), 2)
        part.add_phrase(Phrase())
        self.assertEqual(part.__len__(), 3)

    def test_length(self):
        """Tests Part length() method"""
        part = Part(phrases=[])
        self.assertEqual(part.length(), 0)
        part = Part(phrases=[Phrase(), Phrase(), Phrase()])
        self.assertEqual(part.length(), 3)

    def test_duration(self):
        """Tests Part duration() method"""
        part = Part(phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(part.duration(), 30.0)

        part = Part()
        part.add_phrase(PHRASE_A)  # 10
        part.add_phrase(PHRASE_B, 5.0)  # 15
        part.add_phrase(PHRASE_C)  # 25

        self.assertEqual(part.duration(), 25.0)

    def test_add_phrase(self):
        """Tests Part add_phrase() method"""
        part = Part()
        self.assertEqual(len(part.phrases), 0)

        part.add_phrase(PHRASE_A)
        self.assertEqual(len(part.phrases), 1)
        self.assertEqual(part.duration(), 10.0)

        part.add_phrase(PHRASE_B)
        self.assertEqual(len(part.phrases), 2)
        self.assertEqual(part.duration(), 20.0)

        part.add_phrase(PHRASE_C, 15.0)
        self.assertEqual(len(part.phrases), 3)
        self.assertEqual(part.duration(), 25.0)

    def test_add_phrases(self):
        """Test Part add_phrases() method"""
        part = Part()
        part.add_phrases([PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(len(part.phrases), 3)
        self.assertEqual(
            part.phrases, [(0.0, PHRASE_A), (10.0, PHRASE_B), (20.0, PHRASE_C)]
        )

        part = Part()
        part.add_phrases([PHRASE_A, PHRASE_B, PHRASE_C], [0.0, 1.0, 2.0])
        self.assertEqual(
            part.phrases, [(0.0, PHRASE_A), (1.0, PHRASE_B), (2.0, PHRASE_C)]
        )
        self.assertEqual(part.duration(), 12.0)

    def test_remove_phrase(self):
        """Tests Part remove_phrase() method"""
        part = Part(phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        part.remove_phrase(PHRASE_B)
        self.assertEqual(part.phrases, [(0.0, PHRASE_A), (20.0, PHRASE_C)])

    def test_clear(self):
        """Tests Part clear() method"""
        part = Part(phrases=[PHRASE_A, PHRASE_B, PHRASE_C])
        self.assertEqual(len(part.phrases), 3)
        part.clear()
        self.assertEqual(len(part.phrases), 0)
