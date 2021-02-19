# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:36
import os
from pathlib import Path


class Calculator:
    # @staticmethod
    # def add(a: int, b: int) -> int:
    #     """
    #     Adding numbers
    #     :param a: Number 1
    #     :param b: Number 2
    #     :return: Result of addition
    #     :eq: 4-35
    #     """
    #     return a + b

    @staticmethod
    def uniClassification(a: int):
        """
        University grade calculator
        :param a: grade of student
        :return: str
        :eq: 0-39: 'Failed', 40-100: 'Pass', 'Wrong grade.'
        """
        if 0 <= a < 39:
            return 'Failed'
        elif 40 <= a < 50:
            return 'Pass'
        elif 50 <= a < 60:
            return '2:2'
        elif 60 <= a < 70:
            return '2:1'
        elif 70 <= a <= 100:
            return 'First!'
        else:
            return 'Wrong grade.'

    @staticmethod
    def pairwiseTest(a: str, b: str, c: str):
        if a == 'Brand 1':
            if b == 'a_test1':
                return 'Brand 1, in a_test1'
            if c == 'c_test2':
                return 'Brand 1, in c_test2'
            else:
                return 'Brand 1, not in test1'
        elif a == 'Brand 2':
            if b == 'b_test1':
                if c == 'c_test1':
                    return 'Brand 2, in c_test1'
                return 'Brand 2, in b_test1'
            elif b == 'b_test2':
                return 'Brand 2, in b_test2'
            elif b == 'b_test3':
                return 'Brand 2, in b_test3'
            else:
                return 'Brand 2, not in b_test1-2-3'
        else:
            return 'outside of ranges'


def test():
    pass


if __name__ == '__main__':
    calc = Calculator()
    print(calc.uniClassification(34))
    print('.'.join(__name__.split('.')[:-1]))
