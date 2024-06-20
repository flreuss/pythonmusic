import unittest
from pythonmusic.music import Note, Rest

PITCH = 50
DURATION = 1.0
DYNAMIC = 127

# TODO: replace with constant
REST = -1


class NoteTests(unittest.TestCase):
    def test_init(self):
        """Test Note.__init__"""

        note = Note(0, DURATION, DYNAMIC)
        note = Note(REST, DURATION, DYNAMIC)
        note = Note(PITCH, DURATION, DYNAMIC)

        self.assertEqual(note.pitch, PITCH)
        self.assertEqual(note.duration, DURATION)
        self.assertEqual(note.dynamic, DYNAMIC)

    def test_range_check_pitch_above(self):
        """Test Note.__init__ and propery out of bounds pitch (above)"""
        with self.assertRaises(ValueError):
            _ = Note(127 + 1, DURATION, DYNAMIC)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.pitch = 127 + 1

    def test_range_check_pitch_below(self):
        """Test Note.__init__ and property out of bounds pitch (below)"""
        with self.assertRaises(ValueError):
            _ = Note(-20, DURATION, DYNAMIC)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.pitch = -20

    def test_range_check_dynamic_above(self):
        """Test Note.__init__ and property out of bounds dynamic (above)"""
        with self.assertRaises(ValueError):
            _ = Note(PITCH, DURATION, 127 + 1)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.dynamic = 127 + 1

    def test_range_check_dynamic_below(self):
        """Test Note.__init__ and property out of bounds dynamic (below)"""
        with self.assertRaises(ValueError):
            _ = Note(PITCH, DURATION, -1)
        with self.assertRaises(ValueError):
            note = Note(PITCH, DURATION, DYNAMIC)
            note.dynamic = -20

    def test_str(self):
        """Test Note.__str__"""
        note = Note(30, 1.0, 40)
        self.assertEqual(note.__str__(), "Note(30, 1.0, 40)")

    def test_eq(self):
        """Test Note.__eq__"""
        note_a = Note(PITCH, DURATION, DYNAMIC)
        note_b = Note(PITCH, DURATION, DYNAMIC)

        self.assertEqual(note_a, note_b)

    def test_is_rest(self):
        """Test Note().is_rest"""
        note = Note(PITCH, DURATION, DYNAMIC)
        self.assertFalse(note.is_rest())

        rest = Note.rest(DURATION)
        self.assertTrue(rest.is_rest())

        rest = Note(REST, DURATION, DYNAMIC)
        self.assertTrue(rest.is_rest())

        rest = Rest(DURATION)
        self.assertTrue(rest.is_rest())

    def test_as_rest(self):
        """Test Note().as_rest"""
        note = Note(PITCH, DURATION, DYNAMIC)
        rest = note.as_rest()

        self.assertEqual(rest.pitch, REST)
        self.assertEqual(rest.duration, DURATION)
        self.assertEqual(rest.dynamic, DYNAMIC)
