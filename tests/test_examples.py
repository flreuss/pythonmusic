import unittest


class ExampleScoreTests(unittest.TestCase):
    def test_prelude_in_c(self):
        """Simple test if prelude in c example throws errors"""
        import examples.songs.prelude_in_c as prelude

        score = prelude.make_score()
        # does not test contents, simply listen to them!
        self.assertIsNotNone(score)
