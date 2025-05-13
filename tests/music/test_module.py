import unittest

from pythonmusic.constants.articulations import LEGATO
from pythonmusic.music import Note, dotted, flat, legato_l, sharp


class MusicModuleTests(unittest.TestCase):
    def test_sharp(self):
        self.assertEqual(sharp(5), 6)

    def test_flat(self):
        self.assertEqual(flat(5), 4)

    def test_dotted(self):
        self.assertEqual(dotted(1.0, 1), 1.5)
        self.assertEqual(dotted(1.0, 2), 1.75)

    def test_legato_l(self):
        # also applies to legao (non_l) version
        notes = [Note(60, 1.0), Note(62, 1.0), Note(63, 1.0), Note(65, 3.0)]
        notes_l = legato_l(notes)

        for note in notes_l:
            self.assertTrue(note.has_articulation(LEGATO))
