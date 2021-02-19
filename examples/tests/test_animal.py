import animal
from animal import Animal
import foo
from foo import Bar
from foo import Foo
from mock import patch
import pet
from pet import Animal
from pet import Pet
import random
from random import Random
import unittest


class AnimalTest(unittest.TestCase):
    def test_get_age(self):
        animal_instance = Animal('Dog', 12)
        self.assertEqual(
            animal_instance.get_age(),
            12
        )

    @patch.object(Random, '__init__')
    def test_get_complex_object(self, mock___init__):
        mock___init__.return_value = None
        animal_instance = Animal('Dog', 12)
        self.assertIsInstance(
            animal_instance.get_complex_object(),
            random.Random
        )

    def test_get_species(self):
        animal_instance = Animal('Dog', 12)
        self.assertEqual(
            animal_instance.get_species(),
            'Dog'
        )


if __name__ == "__main__":
    unittest.main()
