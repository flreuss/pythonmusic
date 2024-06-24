import unittest
from pythonmusic.music.note import Note
from pythonmusic.music.phrase import Phrase
from pythonmusic.music.part import Part
from pythonmusic.constants import *


class PartTests(unittest.TestCase):
    def test_init(self):
        """Tests Part initialiser"""
        part = Part()
        self.assertEqual(part.title, None)
        self.assertEqual(part.instrument, instruments.ACOUSTIC_GRAND_PIANO)
        self.assertEqual(part.channel, 1)
        self.assertEqual(part.phrases, [])
        self.assertEqual(part.panning, panning.PAN_CENTER)

        phrase = Phrase([Note(1, 1), Note(2, 2)])
        part = Part(
            title="Harpsichord",
            instrument=instruments.HARPSICHORD,
            channel=5,
            phrases=[phrase],
            panning=panning.PAN_LEFT,
        )
        self.assertEqual(part.title, "Harpsichord")
        self.assertEqual(part.instrument, instruments.HARPSICHORD)
        self.assertEqual(part.channel, 5)
        # test for add_phrases tests this more in depth
        self.assertEqual(part.phrases, [(0, phrase)])
        self.assertEqual(part.panning, panning.PAN_LEFT)

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
        phrase_a = Phrase([Note(1, 5.0), Note(1, 4.0), Note(1, 1.0)])
        phrase_b = Phrase([Note(1, 10.0)])
        phrase_c = Phrase([Note(1, 5.0), Note(1, 5.0)])

        part = Part(phrases=[phrase_a, phrase_b, phrase_c])
        self.assertEqual(part.duration(), 30.0)

        part = Part()
        part.add_phrase(phrase_a)  # 10
        part.add_phrase(phrase_b, 5.0)  # 15
        part.add_phrase(phrase_c)  # 25

        self.assertEqual(part.duration(), 25.0)
