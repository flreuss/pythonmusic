import unittest
from pythonmusic.music.note import Note
from pythonmusic.music.phrase import Phrase
from pythonmusic.constants.pitches import *
from pythonmusic.constants.durations import *
from pythonmusic.constants.dynamics import *

NOTES = [
    Note(C3, QN, F),
    Note(E3, QN, PP),
    Note(G4, DEN, MF),
    Note(G4, SN, FF),
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
        """Tests Phrase initialiser"""
        phrase = Phrase()
        self.assertEqual(phrase.notes.__len__(), 0)

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.notes.__len__(), NOTES.__len__())

    def test_eq(self):
        """Tests Phrase eq"""
        phrase = Phrase()
        self.assertIsNot(phrase, Phrase())
        self.assertEqual(phrase, Phrase())

        phrase.add_notes(NOTES)
        self.assertIsNot(phrase, Phrase(NOTES))
        self.assertEqual(phrase, Phrase(NOTES))

        phrase.add_note(Note(A3, QN))
        self.assertIsNot(phrase, Phrase(NOTES))
        self.assertNotEqual(phrase, Phrase(NOTES))

    def test_separation_input_array(self):
        """
        Tests that the list of notes given to the initialiser is (deep) copied.
        """
        notes = [Note(1, 1, 1), Note(2, 2, 2)]
        phrase = Phrase(notes)

        self.assertIsNot(notes, phrase.notes)

        notes.append(Note(3, 3, 3))
        self.assertNotEqual(len(notes), len(phrase.notes))

    def test_len(self):
        """Tests Phrase __len__() dunder method"""
        phrase = Phrase(NOTES)
        self.assertEqual(phrase.notes.__len__(), NOTES.__len__())

        phrase.add_note(Note(0, 0))
        self.assertEqual(phrase.notes.__len__(), NOTES.__len__() + 1)

    def test_length(self):
        """Tests Phrase length() method"""
        phrase = Phrase(NOTES)
        self.assertEqual(phrase.length(), NOTES.__len__())

        phrase.add_note(Note(0, 0))
        self.assertEqual(phrase.length(), NOTES.__len__() + 1)

    def test_duration(self):
        """Tests Phrase duration property"""
        notes = [Note(0, 1.0), Note(30, 0.5), Note(15, 56.0)]
        expected_duration = 1.0 + 0.5 + 56.0
        phrase = Phrase(notes)

        self.assertEqual(phrase.duration, expected_duration)

        notes.append(Note(0, 100.0))
        expected_duration += 100.0
        phrase = Phrase(notes)

    def test_add_note(self):
        """Tests Note add_note() method"""
        phrase = Phrase()
        self.assertEqual(len(phrase), 0)

        note = Note(1, 1, 1)
        phrase.add_note(note)
        self.assertEqual(len(phrase), 1)
        self.assertEqual(phrase.notes[0], note)

        notes = list(
            map(lambda i: Note(i % 127, float(i), i % 127), range(1000))
        )

        phrase = Phrase()
        for note in notes:
            phrase.add_note(note)

        self.assertEqual(notes, phrase.notes)

    def test_notes(self):
        """Tests Note add_notes() method"""
        notes = list(
            map(lambda i: Note(i % 127, float(i), i % 127), range(1000))
        )

        phrase = Phrase()
        phrase.add_notes(notes)

        self.assertEqual(notes, phrase.notes)

    def test_add_notes_by_lists_valid(self):
        """
        Tests Note add_notes_by_lists() method in a valid case (parallel lists)
        """
        RANGE_MAX = 127
        pitches = list(range(RANGE_MAX))
        durations = list(map(lambda x: float(x * 2), pitches))
        dynamics = list(map(lambda i: (i * 2) % 127, range(RANGE_MAX)))
        notes = list(
            map(
                lambda i: Note(pitches[i], durations[i], dynamics[i]),
                range(RANGE_MAX),
            )
        )

        phrase = Phrase()
        phrase.add_notes_by_lists(pitches, durations, dynamics)

        self.assertEqual(phrase.notes, notes)

    def test_add_notes_by_lists_invalid(self):
        """
        Tests that Note method add_notes_by_lists() throws if the given lists are
        not equal in length and, thus, parallel
        """
        with self.assertRaises(ValueError):
            Phrase().add_notes_by_lists([1, 2, 3], [3.0], [1, 2, 3])
        with self.assertRaises(ValueError):
            Phrase().add_notes_by_lists([1, 2], [3.0, 4.0, 2.0], [1, 2, 3])
        with self.assertRaises(ValueError):
            Phrase().add_notes_by_lists([1, 2, 3], [3.0, 5.0, 7.0], [1, 2])

    def test_remove_note_valid(self):
        """Tests Note remove_note() method"""
        phrase = Phrase(NOTES)
        phrase.remove_note(0)
        self.assertEqual(phrase.notes, NOTES[1:])

    def test_remove_note_invalid(self):
        """
        Tests Note remove_note() method in case that an invalid index is given
        """
        INVALID_INDEX = 1000
        phrase = Phrase(NOTES)
        self.assertLess(len(NOTES), INVALID_INDEX)

        with self.assertRaises(IndexError):
            phrase.remove_note(INVALID_INDEX)

    def test_clear(self):
        """Tests Note clear() method"""
        phrase = Phrase(NOTES)
        self.assertEqual(len(NOTES), len(phrase))

        phrase.clear()
        self.assertEqual(0, len(phrase))

    def test_min_pitch(self):
        """Tests Note min_pitch() method"""
        phrase = Phrase()
        self.assertIsNone(phrase.min_pitch())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.min_pitch(), C3)

    def test_max_pitch(self):
        """Tests Note max_pitch() method"""
        phrase = Phrase()
        self.assertIsNone(phrase.max_pitch())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.max_pitch(), D5)

    def test_min_duration(self):
        """Tests Note min_duration method"""
        phrase = Phrase()
        self.assertIsNone(phrase.min_duration())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.min_duration(), SN)

    def test_max_duration(self):
        """Tests Note max_duration method"""
        phrase = Phrase()
        self.assertIsNone(phrase.max_duration())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.max_duration(), HN)

    def test_min_dynamic(self):
        """Tests Note min_dynamic method"""
        phrase = Phrase()
        self.assertIsNone(phrase.min_dynamic())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.min_dynamic(), PP)

    def test_max_dynamic(self):
        """Tests Note max_dynamic method"""
        phrase = Phrase()
        self.assertIsNone(phrase.max_dynamic())

        phrase = Phrase(NOTES)
        self.assertEqual(phrase.max_dynamic(), FF)
