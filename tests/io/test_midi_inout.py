import unittest
from pythonmusic.io import MidiSender, MidiReceiver


class MidiInOutTests(unittest.TestCase):
    def test_init_midi_sender(self):
        _ = MidiSender()

    def test_init_midi_receiver(self):
        _ = MidiReceiver()
