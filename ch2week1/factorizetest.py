import unittest

def factorize(x):
    """ 
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)

        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)
    
    def test_negative(self):
        cases = (-1, -10, -100)

        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = (0, 1)

        for x in cases:
            with self.subTest(case=x):
                a = factorize(x)
                self.assertEqual(a,(x,))

    def simpe_numbers(self):
        cases = (13, 3, 29)

        for x in cases:
            with self.subTest(case=x):
                a = factorize(x)
                self.assertEqual(a,(x,))

    def test_two_simple_multipliers(self):
        cases = (6, 26, 121)

        for x in cases:
            with self.subTest(case=x):
                a = factorize(x)
                self.assertEqual(len(a),2)

    def test_many_multipliers(self):
        cases = (1001, 9699690)

        for x in cases:
            with self.subTest(case=x):
                a = factorize(x)
                self.assertGreater(len(a),2)

if __name__ == "__main__":
    unittest.main()