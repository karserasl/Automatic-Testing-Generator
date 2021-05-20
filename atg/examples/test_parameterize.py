#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from allpairspy import AllPairs


def function_to_be_tested(brand, operating_system, minute):
    # do something

    return True


def carDeals(brand: str, price: int, cond: str):
    if brand == "Ford":
        if price >= 20000 and cond == "New":
            return "Good Deal"
        elif price < 20000 and cond == 'Used':
            return 'Bad Deal'
        else:
            return 'Could be better'
    if brand == "BMW":
        if price >= 50000 and cond == "Used":
            return 'Bad Deal'
        elif price >= 40000 and (cond == 'New' or cond == 'Used'):
            return 'Could be better'
        else:
            return 'Good Deal'
    if brand == 'Volvo':
        if cond == 'New' and price < 40000:
            return 'Good Deal'
        else:
            return 'Could be better'


class TestParameterized:
    parameters = [
        ["Ford", "Volvo", "BMW"],
        [20000, 40000, 50000],
        ["New", "Used"]]

    ans = ['Good Deal', 'Could be better', 'Could be better', 'Could be better', 'Could be better', 'Bad Deal',
           'Bad Deal', 'Could be better', 'Good Deal']

    list = [value_list for value_list in AllPairs(parameters)]

    @pytest.mark.parametrize(
        list, ans
    )
    # def test(self, brand, operating_system, minute):
    #     assert function_to_be_tested(brand, operating_system, minute)

    def test(self, brand: str, price: int, cond: str):
            assert carDeals(brand, price, cond)
