# @Author: Administrator
# @Date:   03/02/2021 14:26
import random
import sys

TECH_ID = 'eqv_part'

MODULE_NAME = sys.modules[__name__].__name__.split('.')[-1]
PACKAGE_NAME = sys.modules[__name__].__name__.split('.')[-2]


def get_eq_partitions(partitions: dict) -> dict:
    result = {}
    for part, res in partitions.items():
        if '-' in part:
            p = list(map(int, part.split('-')))
            result[random.randint(p[0] + 2, p[1] - 2)] = res
        else:
            result[part] = res
    return result
