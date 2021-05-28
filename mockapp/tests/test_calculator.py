from calculator import not_method
from itertools import combinations
import random
import unittest


class NotMethod(unittest.TestCase):
    # ------------------------------------ not_method - function ----------------------------------- #
    def test_not_method_0(self):
        self.assertEqual(
            not_method(*['t', 5]),
            "test 1")

    def test_not_method_1(self):
        self.assertEqual(
            not_method(*['a', 14]),
            "test 2")


if __name__ == "__main__":
    unittest.main()
