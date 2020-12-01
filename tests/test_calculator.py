# @Author: Lampros.Karseras
# @Date:   17/11/2020 09:46

from mockapp import calculator
import unittest


class CalcTest(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = calculator.Calculator()

    def test_add(self):
        self.assertEqual(
            self.calc.add(a=5, b=4),
            9,
            msg="5+4 should equal 9."
        )
