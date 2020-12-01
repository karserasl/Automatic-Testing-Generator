# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:47
import mockapp.calculator as calc
from docstring_parser import parse
from atg.parse_docstrings import parse_docstring


def generate_testcase(func):
    def func_wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        print('assert %s(%s) == %s' % (func.__name__, ', '.join(repr(arg) for arg in args), return_value))
        return return_value

    return func_wrapper


@generate_testcase
def square(x):
    return x ** 2


if __name__ == '__main__':
    # print(square(3) + square(4) == square(5))
    calc.Calculator.uniClassification(51)
    doc = parse_docstring(calc.Calculator.uniClassification.__doc__)
