import unittest
from math import floor
from typing import Self

import pythonmusic.constants.pitches as pitches
from pythonmusic.music import sharp
from pythonmusic.util import *


class UtilTests(unittest.TestCase):
    def test_assert_range(self):
        assert_range(56, 0, 100)
        assert_range(34, -12, 45)

        assert_range(10, 10, 10)
        assert_range(10, 10, 11)
        assert_range(10, 9, 10)
        assert_range(9, 9, 10)

        assert_range(56.0, 0.0, 100.0)
        assert_range(34.0, -12.0, 45.0)

        assert_range(10.0, 10.0, 10.0)
        assert_range(10.0, 10.0, 11.0)
        assert_range(10.0, 9.0, 10.0)
        assert_range(9.0, 9.0, 10.0)

    def test_clip(self):
        self.assertEqual(clip(34, 0, 100), 34)
        self.assertEqual(clip(45.1, 0.5, 45.0), 45.0)
        self.assertEqual(clip(0, 10, 20), 10)

    def test_make_instrument(self):
        i = make_instrument(1, 0)
        j = 1
        self.assertEqual(i, j)

        i = make_instrument(1, 1)
        j = (1 << 8) | 1
        self.assertEqual(i, j)

        i = make_instrument(127, 2)
        j = (2 << 8) | 127
        self.assertEqual(i, j)

    def test_instrument_get_patch_bank(self):
        i = make_instrument(120, 5)
        self.assertEqual(instrument_get_patch_bank(i), (120, 5))

        i = make_instrument(8, 2)
        self.assertEqual(instrument_get_patch_bank(i), (8, 2))

        i = make_instrument(7, 8)
        self.assertEqual(instrument_get_patch_bank(i), (7, 8))

    def test_find_pattern(self):
        self.assertEqual(find_pattern("ter", ["a", "meter", "b", "meter2"]), "meter")
        self.assertEqual(find_pattern("b", ["a", "meter", "b", "meter2"]), "b")
        self.assertEqual(find_pattern("9", ["a", "meter", "b", "meter2"]), None)
        self.assertEqual(find_pattern("2", ["a", "meter", "b", "meter2"]), "meter2")

    def test_find_pattern_index(self):
        self.assertEqual(find_pattern_index("ter", ["a", "meter", "b", "meter2"]), 1)
        self.assertEqual(find_pattern_index("b", ["a", "meter", "b", "meter2"]), 2)
        self.assertEqual(find_pattern_index("9", ["a", "meter", "b", "meter2"]), None)
        self.assertEqual(find_pattern_index("2", ["a", "meter", "b", "meter2"]), 3)

    def test_map_value(self):
        result = map_value(50, 0, 100, 0, 1000)
        self.assertEqual(result, 500)

        result = map_value(5, 0, 10, 0, 5)
        self.assertEqual(result, 2)  # rounds down
        result = map_value(5, 0, 10, 0, 5, conversion_strategy=floor)
        self.assertEqual(result, 2)

        result = map_value(6, -10, 10, 0, 100)
        self.assertEqual(result, 80)

        result = map_value(6, -11, 10, 0, 100)
        self.assertEqual(result, 81)
        result = map_value(6, -11, 10, 0, 100, conversion_strategy=floor)
        self.assertEqual(result, 80)

    def test_mpqn_bpm_conversion(self):
        bpm = 120
        self.assertEqual(mpqn_to_bpm(bpm_to_mpqn(bpm)), bpm)

    def test_beats_to_ticks(self):
        _PPQ = 960
        self.assertEqual(beats_to_ticks(4.0, _PPQ), 3840)
        self.assertEqual(beats_to_ticks(4.32, _PPQ), 4147)

    def test_pitch_to_key(self):
        self.assertEqual(frequency_to_key(261.6256), pitches.C4)
        self.assertEqual(frequency_to_key(440.0), pitches.A4)
        self.assertEqual(frequency_to_key(1567.982), pitches.G6)
        self.assertEqual(frequency_to_key(7902.133), pitches.B8)

    def test_key_to_pich(self):
        self.assertAlmostEqual(key_to_frequency(pitches.A4), 440.0, 2)
        self.assertAlmostEqual(key_to_frequency(sharp(pitches.A4)), 466.1638, 4)
        self.assertAlmostEqual(key_to_frequency(pitches.F6), 1396.913, 3)
        self.assertAlmostEqual(key_to_frequency(pitches.A0), 27.5, 2)

    def test_contains_identity(self):
        class TestClass:
            pass

        a = TestClass()
        b = TestClass()

        self.assertTrue(contains_identity([a, b], a))
        self.assertFalse(contains_identity([b, b], a))

    def test_int_to_vlq(self):
        self.assertEqual(int_to_vlq(0), bytes([0x00]))
        self.assertEqual(int_to_vlq(0b0_1101111), bytes([0b01101111]))
        self.assertEqual(
            int_to_vlq(0b00_1111111_1101111),
            bytes([0b11111111, 0b01101111]),
        )
        self.assertEqual(
            int_to_vlq(0x0F4240),
            bytes([0xBD, 0x84, 0x40]),
        )

    def test_vlc_to_int(self):
        self.assertEqual(vlq_to_int(bytes(0)), 0x00)
        self.assertEqual(vlq_to_int(bytes([0b01101111])), 0b01101111)
        self.assertEqual(
            vlq_to_int(bytes([0b11111111, 0b01101111])), 0b00_1111111_1101111
        )
        self.assertEqual(vlq_to_int(bytes([0xBD, 0x84, 0x40])), 0x0F4240)
