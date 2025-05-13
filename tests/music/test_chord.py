import unittest
from copy import deepcopy

from pythonmusic.constants.chords import *
from pythonmusic.constants.durations import *
from pythonmusic.constants.dynamics import *
from pythonmusic.constants.pitches import *
from pythonmusic.music import Chord, Note

NOTES = [
    Note(C3, QN, F),
    Note(E3, QN, PP),
    Note(G4, DEN, MF),
    Note(G4, SN, FF),
    Note(C5, DEN),
    Note(C5, SN),
]


class ChordTests(unittest.TestCase):
    def test_init(self):
        chord = Chord(NOTES)

        self.assertEqual(len(chord), len(NOTES))
        self.assertTrue(chord.is_chord())

    def test_iter(self):
        notes = list(map(lambda x: Note(2 * x, x), range(50)))
        self.assertEqual(notes, list(Chord(notes).__iter__()))

    def test_from_root(self):
        notes = [
            Note(C4, QN),
            Note(E4, QN),
            Note(G4, QN),
        ]

        chord = Chord.from_root(C4, MAJOR, QN)
        self.assertEqual(chord.notes, Chord(notes).notes)

    def test_from_lists(self):
        pitches = [45, 65, 7]
        durations = [3.4, 2.0, 34.0]
        dynamics = [54, 23, 67]

        check = Chord()
        check.add_notes(
            list(
                map(
                    lambda i: Note(pitches[i], durations[i], dynamics[i]),
                    range(len(pitches)),
                )
            )
        )

        chord = Chord.from_lists(pitches, durations, dynamics)
        self.assertEqual(check, chord)

        chord = Chord.from_lists([A4, D4, C4], [QN], [MF, FF])
        self.assertEqual(
            chord.notes, [Note(A4, QN, MF), Note(D4, QN, FF), Note(C4, QN, FF)]
        )

        chord = Chord.from_lists([A4], [QN, EN, SN], [MF, FF])
        self.assertEqual(
            chord.notes, [Note(A4, QN, MF), Note(A4, EN, FF), Note(A4, SN, FF)]
        )

        chord = Chord.from_lists([A4, D4], [QN], [MF, FF, FFF])
        self.assertEqual(
            chord.notes, [Note(A4, QN, MF), Note(D4, QN, FF), Note(D4, QN, FFF)]
        )

    def test_eq(self):
        chord_a = Chord(NOTES)
        chord_b = deepcopy(chord_a)

        self.assertIsNot(chord_a, chord_b)
        self.assertEqual(chord_a, chord_b)

    def test_length(self):
        chord = Chord(NOTES)

        self.assertEqual(len(chord), len(NOTES))

    def test_notes(self):
        chord = Chord(NOTES)
        self.assertEqual(chord.notes, NOTES)

        notes_b = [Note(G4, QN)]
        chord.notes += notes_b
        self.assertEqual(chord.notes, NOTES + notes_b)

    def test_duration(self):
        chord = Chord(NOTES)
        self.assertEqual(chord.duration, QN)

        chord = Chord([Note(C4, QN), Note(D4, HN)])
        self.assertEqual(chord.duration, HN)

    def test_is_note(self):
        chord = Chord(NOTES)
        self.assertFalse(chord.is_note())

    def test_is_chord(self):
        chord = Chord(NOTES)
        self.assertTrue(chord.is_chord())

    def test_add_note(self):
        chord = Chord()
        chord.add_note(Note(G4, QN))
        self.assertEqual(chord, Chord([Note(G4, QN)]))

    def test_add_notes(self):
        chord = Chord()
        chord.add_notes(NOTES)
        self.assertEqual(chord, Chord(NOTES))

    def test_add_notes_by_lists(self):
        chord = Chord()
        chord.add_notes_by_lists([45, 46], [4.0, 5.0], [3, 4])
        self.assertEqual(chord, Chord([Note(45, 4.0, 3), Note(46, 5.0, 4)]))

    def test_remove_notes(self):
        chord = Chord(NOTES)
        chord.remove_note(0)
        self.assertEqual(chord, Chord(NOTES[1:]))

        chord = Chord()
        chord.add_notes([Note(1, 1.0), Note(2, 2.0), Note(3, 3.0)])
        chord.remove_note(1)
        self.assertEqual(chord, Chord([Note(1, 1.0), Note(3, 3.0)]))

    def test_clear(self):
        chord = Chord(NOTES)
        self.assertEqual(len(NOTES), len(chord))

        chord.clear()
        self.assertEqual(0, len(chord))

    def test_min_pitch(self):
        chord = Chord()
        self.assertIsNone(chord.min_pitch())

        chord = Chord(NOTES)
        self.assertEqual(chord.min_pitch(), C3)

    def test_max_pitch(self):
        chord = Chord()
        self.assertIsNone(chord.max_pitch())

        chord = Chord(NOTES)
        self.assertEqual(chord.max_pitch(), C5)

    def test_min_duration(self):
        chord = Chord()
        self.assertIsNone(chord.min_duration())

        chord = Chord(NOTES)
        self.assertEqual(chord.min_duration(), SN)

    def test_max_duration(self):
        chord = Chord()
        self.assertIsNone(chord.max_duration())

        chord = Chord(NOTES)
        self.assertEqual(chord.max_duration(), QN)

    def test_min_dynamic(self):
        chord = Chord()
        self.assertIsNone(chord.min_dynamic())

        chord = Chord(NOTES)
        self.assertEqual(chord.min_dynamic(), PP)

    def test_max_dynamic(self):
        chord = Chord()
        self.assertIsNone(chord.max_dynamic())

        chord = Chord(NOTES)
        self.assertEqual(chord.max_dynamic(), FF)

    def test_flatten(self):
        chord = Chord([Note(C4, EN), Note(C4, EN)])
        self.assertEqual(chord.flatten(), [Note(C4, EN), Note(C4, EN)])

        chord = Chord(
            [Note(C4, EN), Note(C4, EN), Chord([Note(C4, EN), Note(C4, EN)])]  # type: ignore
        )
        self.assertEqual(
            chord.flatten(), [Note(C4, EN), Note(C4, EN), Note(C4, EN), Note(C4, EN)]
        )
