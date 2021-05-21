import calculator
from itertools import combinations
import random
import unittest


class Calculator(unittest.TestCase):
    def setUp(self) -> None:

        self.calculator=calculator.Calculator()
    # ------------------------------------ carDeals - method ----------------------------------- #
    def test_carDeals_0(self):

        self.assertEqual(

            self.calculator.carDeals(*[37]),

            "Failed")
    def test_carDeals_1(self):

        self.assertEqual(

            self.calculator.carDeals(*[44]),

            "Pass")
    def test_carDeals_2(self):

        self.assertEqual(

            self.calculator.carDeals(*[57]),

            "2:2")
    def test_carDeals_3(self):

        self.assertEqual(

            self.calculator.carDeals(*[66]),

            "2:1")
    def test_carDeals_4(self):

        self.assertEqual(

            self.calculator.carDeals(*[88]),

            "First!")
    def test_carDeals_5(self):

        self.assertEqual(

            self.calculator.carDeals(*['Ford', 20000, 'New']),

            "Good Deal")
    def test_carDeals_6(self):

        self.assertEqual(

            self.calculator.carDeals(*['Volvo', 40000, 'New']),

            "Could be better")
    def test_carDeals_7(self):

        self.assertEqual(

            self.calculator.carDeals(*['BMW', 50000, 'New']),

            "Could be better")
    def test_carDeals_8(self):

        self.assertEqual(

            self.calculator.carDeals(*['BMW', 40000, 'Used']),

            "Could be better")
    def test_carDeals_9(self):

        self.assertEqual(

            self.calculator.carDeals(*['Volvo', 20000, 'Used']),

            "Could be better")
    def test_carDeals_10(self):

        self.assertEqual(

            self.calculator.carDeals(*['Ford', 50000, 'Used']),

            "Bad Deal")
    def test_carDeals_11(self):

        self.assertEqual(

            self.calculator.carDeals(*['Ford', 40000, 'Used']),

            "Bad Deal")
    def test_carDeals_12(self):

        self.assertEqual(

            self.calculator.carDeals(*['Volvo', 50000, 'Used']),

            "Could be better")
    def test_carDeals_13(self):

        self.assertEqual(

            self.calculator.carDeals(*['BMW', 20000, 'Used']),

            "Good Deal")
if __name__ == "__main__":
    unittest.main()
