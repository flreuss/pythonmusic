import unittest

from pythonmusic.io import MidiMessage, RawMessage
from pythonmusic.constants import C4, P, NOTE_ON


class MidiMessageTests(unittest.TestCase):
    def test_init(self):
        m = MidiMessage(NOTE_ON, note=C4, velocity=P)
        self.assertEqual(m.type, NOTE_ON)
        self.assertEqual(m["type"], NOTE_ON)
        self.assertEqual(m["note"], C4)
        self.assertEqual(m["velocity"], P)

    def test_from_raw(self):
        r = RawMessage("note_on", note=60)
        m = MidiMessage.from_raw(r)

        self.assertEqual(m["type"], "note_on")
        self.assertEqual(m["note"], 60)

    def test_raw(self):
        m = MidiMessage(NOTE_ON, note=C4, velocity=P)
        r = m.raw()

        self.assertEqual(r.dict()["type"], NOTE_ON)
        self.assertEqual(r.dict()["velocity"], P)
