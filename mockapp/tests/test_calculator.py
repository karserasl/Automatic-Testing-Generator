# @Author: Lampros.Karseras
# @Date:   17/11/2020 09:46

from mockapp import calculator
import unittest


class CalcTest(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = calculator.Calculator()

    def test_add(self):
        self.assertEqual(
            self.calc.add(a=10, b=15),
            25
        )

    def test_uniClassification_1(self):
        self.assertEqual(
            self.calc.uniClassification(4),
            'Failed'
        )

    def test_uniClassification_2(self):
        self.assertEqual(
            self.calc.uniClassification(40),
            'Pass'
        )

    def test_uniClassification_3(self):
        self.assertEqual(
            self.calc.uniClassification(50),
            '2:2'
        )

    def test_uniClassification_4(self):
        self.assertEqual(
            self.calc.uniClassification(60),
            '2:1'
        )

    def test_uniClassification_5(self):
        self.assertEqual(
            self.calc.uniClassification(70),
            'First!'
        )

    def test_uniClassification_6(self):
        self.assertEqual(
            self.calc.uniClassification(101),
            'Wrong grade.'
        )
