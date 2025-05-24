import unittest

from pythonmusic.constants.articulations import LEGATO
from pythonmusic.music import Note, legato_l


class MusicModuleTests(unittest.TestCase):
    def test_legato_l(self):
        # also applies to legao (non_l) version
        notes = [Note(60, 1.0), Note(62, 1.0), Note(63, 1.0), Note(65, 3.0)]
        notes_l = legato_l(notes)

        for note in notes_l:
            self.assertTrue(note.has_articulation(LEGATO))
