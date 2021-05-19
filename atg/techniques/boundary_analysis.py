# @Author: Administrator
# @Date:   03/02/2021 14:26
import random
import sys

TECH_ID = 'bva'

MODULE_NAME = sys.modules[__name__].__name__.split('.')[-1]
PACKAGE_NAME = sys.modules[__name__].__name__.split('.')[-2]


def get_boundaries(outputs: list, inv_choices: str) -> dict:
    boundaries = set()
    result = {}
    for part in outputs:
        output_answer = part.pop()
        str_part = ''.join(part)
        if '-' in str_part:
            p = list(map(int, str_part.split('-')))
            boundaries.update({p[0] - 1, p[0], p[0] + 1, p[1] - 1, p[1], p[1] + 1})
            result.update({i: None for i in sorted(boundaries) if i not in result})
            p = list(map(int, str_part.split('-')))
            if result[p[0] - 1] is None and inv_choices:
                result[p[0] - 1] = inv_choices
            if result[p[1] + 1] is None and inv_choices:
                result[p[1] + 1] = inv_choices
            result[p[0]] = output_answer
            result[p[0] + 1] = output_answer
            result[p[1]] = output_answer
            result[p[1] - 1] = output_answer
    return result


def run(outputs: list, inv_choices: str) -> dict:
    return get_boundaries(outputs, inv_choices)
