import unittest
from ch2week2.game.screensaver import Vec2d

class Vec2dTest(unittest.TestCase):
    def test_summ_of_vectors(self):
        cases = (((1,2), (2,3)), ((50,78),(34, 40)))

        for x in cases:
            with self.subTest(case=x):
                pass
        