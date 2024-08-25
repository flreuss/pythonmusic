import unittest

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

    def test_map_scale(self):
        # NOTE: very difficult to test
        pass
