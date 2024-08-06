import unittest

from pythonmusic.io import _find_pattern as find_pattern


class MidiIoModuleFunctionTests(unittest.TestCase):
    def test_find_pattern_match(self):
        input = ["Hello, world", "Hello, banana", "hello, landscape"]
        pattern = "bana"
        self.assertEqual(find_pattern(input, pattern), "Hello, banana")

        input = [
            "RtMidiIn Client:AReceiver 128:0",
            "RtMidiIn Client:BReceiver 128:1",
            "RtMidiIn Client:BReceiver 124:0",
            "RtMidiIn Client:CReceiver 124:0",
            "RtMidiIn Client:Hello 124:0",
            "RtMidiIn Client:Another 124:0",
        ]
        pattern = "Hello"
        self.assertEqual(find_pattern(input, pattern), "RtMidiIn Client:Hello 124:0")
