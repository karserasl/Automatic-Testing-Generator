import animal
from animal import Animal
import foo
from foo import Bar
from foo import Foo
import functions
from mock import patch
import os
import os.path
import pet
from pet import Animal
from pet import Pet
import random
from random import Random
import unittest


class FunctionsTest(unittest.TestCase):
    @patch.object(os.path, 'exists')
    def test_func_one(self, mock_exists):
        mock_exists.return_value = True
        self.assertEqual(
            functions.func_one(),
            True
        )

    def test_func_three(self):
        self.assertEqual(
            functions.func_three(a='C:/temp'),
            True
        )

    def test_func_two(self):
        self.assertEqual(
            functions.func_two(a='C:/temp'),
            True
        )

    def test_main(self):
        self.assertEqual(
            functions.main(),
            None
        )


if __name__ == "__main__":
    unittest.main()
