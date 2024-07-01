import unittest


class ExampleScoreTests(unittest.TestCase):
    def test_prelude_in_c(self):
        """Simple test if prelude in c example throws errors"""
        import examples.prelude_in_c

        score = examples.prelude_in_c.make_score()
        # does not test contents, simply listen to them!
        self.assertIsNotNone(score)
