# @Author: Lampros.Karseras
# @Date:   04/01/2021 20:44
import random


def getEqPartitions(partitions: dict) -> dict:
    result = {}
    for part, res in partitions.items():
        if '-' in part:
            p = list(map(int, part.split('-')))
            result[random.randint(p[0] + 2, p[1] - 2)] = res
        else:
            result[part] = res
    return result


def getBoundaries(partitions: dict, inv_choices: dict) -> dict:
    boundaries = set()
    for part in partitions.keys():
        if '-' in part:
            p = list(map(int, part.split('-')))
            boundaries.update({p[0] - 1, p[0], p[0] + 1, p[1] - 1, p[1], p[1] + 1})

    result = dict.fromkeys(sorted(boundaries), None)
    for part, res in partitions.items():
        if '-' in part:
            p = list(map(int, part.split('-')))
            if result[p[0] - 1] is None:
                result[p[0] - 1] = inv_choices['errors']
            if result[p[1] + 1] is None:
                result[p[1] + 1] = inv_choices['errors']
            result[p[0]] = res
            result[p[0] + 1] = res
            result[p[1]] = res
            result[p[1] - 1] = res
    return result


def createPartitions(partitions: dict, inv_choices: dict) -> dict:
    return {
        'EqP': getEqPartitions(partitions),

        'Boundaries': getBoundaries(partitions, inv_choices)
    }
