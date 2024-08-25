import unittest

from pythonmusic.helpers import *


class HelperTests(unittest.TestCase):
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
