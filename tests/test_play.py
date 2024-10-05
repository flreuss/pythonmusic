import unittest
from pythonmusic.play import _encode_timing, _decode_timing


class PlayTests(unittest.TestCase):
    def test_encode_timing(self):
        base = 1.432
        code = _encode_timing(base)
        self.assertEqual(code, 143_200)

        base = 1.43232545343645
        code = _encode_timing(base)
        self.assertEqual(code, 143_232)

    def test_decode_timing(self):
        base = 665_873
        code = _decode_timing(base)
        self.assertEqual(code, 6.65873)

        base = 23_442_379
        code = _decode_timing(base)
        self.assertEqual(code, 234.42379)

    def test_bidirectional(self):
        base_a = 1234.34895
        code_a = _encode_timing(base_a)
        self.assertEqual(base_a, _decode_timing(code_a))

        base_b = 579384
        code_b = _decode_timing(base_b)
        self.assertEqual(base_b, _encode_timing(code_b))
