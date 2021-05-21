# @Author: Administrator
# @Date:   21/05/2021 08:01
from unittest import TestCase
from techniques.pairwise import run
import unittest


class Test(TestCase):
    def test_correct(self):
        inputs = [["Ford", "Volvo", "BMW"], [20000, 40000, 50000], ["New", "Used", "test"]]
        expected = [
            ['Ford', 20000, 'New'],
            ['Volvo', 40000, 'New'],
            ['BMW', 50000, 'New'],
            ['BMW', 40000, 'Used'],
            ['Volvo', 20000, 'Used'],
            ['Ford', 50000, 'Used'],
            ['Ford', 40000, 'test'],
            ['Volvo', 50000, 'test'],
            ['BMW', 20000, 'test'],
        ]

        for i, pairs in enumerate(run(inputs)):
            self.assertEqual(
                pairs, expected[i]
            )


if __name__ == '__main__':
    unittest.main()
