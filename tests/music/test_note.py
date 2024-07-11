from copy import deepcopy
import unittest
from pythonmusic.music import Note
from pythonmusic.constants.pitches import REST
from pythonmusic.constants.articulations import (
    LEGATO,
    STACCATO,
    MARCATO,
    PORTATO,
)

PITCH = 50
DURATION = 1.0
DYNAMIC = 127


class NoteTests(unittest.TestCase):
    def test_init(self):
        """Tests initialiser of Note"""

        note = Note(0, DURATION, DYNAMIC)
        note = Note(REST, DURATION, DYNAMIC)
        note = Note(PITCH, DURATION, DYNAMIC)

        self.assertEqual(note.pitch, PITCH)
        self.assertEqual(note.duration, DURATION)
        self.assertEqual(note.dynamic, DYNAMIC)

        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO, STACCATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(STACCATO))
        self.assertTrue(note.has_articulation(PORTATO))
        self.assertFalse(note.has_articulation(MARCATO))

    def test_range_check_pitch_above(self):
        """Tests Note initialiser with an above out of bounds pitch"""
        with self.assertRaises(ValueError):
            _ = Note(127 + 1, DURATION, DYNAMIC)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.pitch = 127 + 1

    def test_range_check_pitch_below(self):
        """Tests Note initialiser with a below out of range pitch"""
        with self.assertRaises(ValueError):
            _ = Note(-20, DURATION, DYNAMIC)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.pitch = -20

    def test_range_check_dynamic_above(self):
        """Tests Note initialiser with an above out of bounds dynamic"""
        with self.assertRaises(ValueError):
            _ = Note(PITCH, DURATION, 127 + 1)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.dynamic = 127 + 1

    def test_range_check_dynamic_below(self):
        """Tests Note initialiser with a below out of bounds dynamic"""
        with self.assertRaises(ValueError):
            _ = Note(PITCH, DURATION, -1)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.dynamic = -20

    def test_is_note(self):
        """Tests Note is_note() method override from abc"""
        note = Note(34, 5.0, 45)
        self.assertTrue(note.is_note())

    def test_is_chord(self):
        """Tests Note is_chord() method override from abc"""
        note = Note(34, 5.0, 45)
        self.assertFalse(note.is_chord())

    def test_eq(self):
        """Tests Note __eq__ dunder method"""
        note_a = Note(PITCH, DURATION, DYNAMIC)
        note_b = Note(PITCH, DURATION, DYNAMIC)

        self.assertEqual(note_a, note_b)

        notes_a = [Note(x, float(x * 2)) for x in range(100)]
        notes_b = deepcopy(notes_a)

        # asserts that identity is different
        self.assertEqual(len(notes_a), len(notes_b))
        for i in range(len(notes_a)):
            self.assertIsNot(notes_a[i], notes_b[i])

        self.assertEqual(notes_a, notes_b)

    def test_is_rest(self):
        """Tests Note is_rest() check"""
        note = Note(PITCH, DURATION, DYNAMIC)
        self.assertFalse(note.is_rest())

        note = Note(REST, DURATION, DYNAMIC)

        rest = Note.rest(DURATION)
        self.assertTrue(rest.is_rest())

    def test_as_rest(self):
        """Tests that Note as_rest() returns a valid rest"""
        note = Note(PITCH, DURATION, DYNAMIC)
        rest = note.as_rest()

        self.assertEqual(rest.duration, DURATION)
        self.assertEqual(rest.dynamic, DYNAMIC)

    def test_add_articulation(self):
        """Tests Note add_articulation() method"""
        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertFalse(note.has_articulation(PORTATO))

    def test_remove_articulation(self):
        """Tests Note remove_articulation() method"""
        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO, MARCATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(MARCATO))
        self.assertFalse(note.has_articulation(PORTATO))

        note.remove_articulation(MARCATO)

        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertFalse(note.has_articulation(MARCATO))
        self.assertFalse(note.has_articulation(PORTATO))

    def test_has_articulation(self):
        """Tests Note has_articulation() method"""
        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO, MARCATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(MARCATO))
        self.assertFalse(note.has_articulation(PORTATO))

    def test_portato_articulation(self):
        """Tests that composite articulation portato works"""
        note = Note(PITCH, DURATION, DYNAMIC, [LEGATO, MARCATO])
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertFalse(note.has_articulation(STACCATO))
        self.assertFalse(note.has_articulation(PORTATO))

        note.add_articulation(STACCATO)
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(STACCATO))
        self.assertTrue(note.has_articulation(PORTATO))

        note.remove_articulation(LEGATO)
        self.assertFalse(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(STACCATO))
        self.assertFalse(note.has_articulation(PORTATO))

        note.add_articulation(LEGATO)
        self.assertTrue(note.has_articulation(LEGATO))
        self.assertTrue(note.has_articulation(STACCATO))
        self.assertTrue(note.has_articulation(PORTATO))

        note.remove_articulation(PORTATO)
        self.assertFalse(note.has_articulation(LEGATO))
        self.assertFalse(note.has_articulation(STACCATO))
        self.assertFalse(note.has_articulation(PORTATO))
