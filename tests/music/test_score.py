import unittest
from copy import deepcopy
from pythonmusic.music import Score, Part, Phrase, Note
from pythonmusic.constants.pitches import *
from pythonmusic.constants.durations import *
from pythonmusic.constants.dynamics import *

PART_A = Part(
    "Part A",
    phrases=[
        Phrase(
            [
                Note(D4, QN, MF),
                Note(EF4, DHN, F),
                Note(C4, QN, F),
                Note(D4, WN, F),
            ]
        )
    ],
)

PART_B = Part(
    "Part B",
    phrases=[
        Phrase(
            [
                Note(BF4, QN, MF),
                Note(C5, DHN, F),
            ]
        ),
        Phrase([Note(A3, QN, F), Note(BF4, WN, F)]),
    ],
)

PART_C = Part(
    "Part C",
    phrases=[
        Phrase(
            [
                Note(G3, QN, MF),
                Note(G3, DHN, F),
                Note(F3, QN, F),
                Note(G3, WN, F),
            ]
        )
    ],
)


class ScoreTests(unittest.TestCase):
    def test_init(self):
        """Tests Score init dunder"""
        TITLE = "Walpurgisnacht"
        PARTS = [PART_A, PART_B, PART_C]
        TEMPO = 120
        score = Score(TITLE, PARTS, TEMPO)

        self.assertEqual(score.title, TITLE)
        self.assertEqual(score.parts, PARTS)
        self.assertEqual(score.tempo, TEMPO)

    def test_len(self):
        """Tests Score __len__() dunder"""
        score = Score("A", [PART_A, PART_B])
        self.assertEqual(score.__len__(), 2)

    def test_length(self):
        """Tests Score length() method"""
        score = Score("A", [PART_A, PART_B])
        self.assertEqual(score.length(), 2)

    def test_duration(self):
        """Tests Score duration() method"""
        new_part = deepcopy(PART_A)
        new_part.add_phrase(Phrase([Note(1, 10.0)]))
        score = Score("", parts=[PART_B, new_part])
        self.assertEqual(score.duration(), 19.0)

    def test_has_part(self):
        """Tests Score has_part() method"""
        score = Score("Test Score", parts=[PART_A, PART_B])
        self.assertTrue(score.has_part(PART_A))
        self.assertTrue(score.has_part(PART_B))
        self.assertFalse(score.has_part(PART_C))

    def test_add_part(self):
        """Tests Score add_part() method"""
        score = Score("Test Score")
        score.add_part(PART_A)
        self.assertTrue(score.has_part(PART_A))

        with self.assertRaises(ValueError):
            score.add_part(PART_A)

    def test_add_parts(self):
        """Tests Score add_parts() method"""
        score = Score("Test Score")
        score.add_parts([PART_A, PART_B])
        self.assertTrue(score.has_part(PART_A))
        self.assertTrue(score.has_part(PART_B))

    def test_remove_part(self):
        """Tests Score remove_part() method"""
        score = Score("Test Score", parts=[PART_A, PART_B, PART_C])
        score.remove_part(PART_B)
        self.assertTrue(score.has_part(PART_A))
        self.assertFalse(score.has_part(PART_B))
        self.assertTrue(score.has_part(PART_C))

    def test_remove_part_by_index(self):
        """Tests Score remove_part_by_index() method"""
        score = Score("Test Score", parts=[PART_A, PART_B, PART_C])
        score.remove_part_by_index(1)
        self.assertTrue(score.has_part(PART_A))
        self.assertFalse(score.has_part(PART_B))
        self.assertTrue(score.has_part(PART_C))

    def test_clear(self):
        """Tests Score clear() method"""
        score = Score("Test Score", parts=[PART_A, PART_B, PART_C])
        score.clear()
        self.assertEqual(score.length(), 0)
