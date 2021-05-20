# @Author: Administrator
# @Date:   03/02/2021 14:26
import random
import sys
from copy import deepcopy
from typing import Optional
import logging
import inspect

logger = logging.getLogger(__name__)

TECH_ID = 'eqv'

MODULE_NAME = sys.modules[__name__].__name__.split('.')[-1]
PACKAGE_NAME = sys.modules[__name__].__name__.split('.')[-2]


def get_eq_partitions(outputs: list, inv_choices: str) -> list:
    process_output = []

    def process_partitions(partition):
        p = list(map(int, partition.split('-')))
        try:
            if p[1] - p[0] < 5:
                rand = random.randint(p[0], p[1])
            else:
                rand = random.randint(p[0] + 2, p[1] - 2)
            result.append(rand)
        except ValueError as e:
            logger.error(f'Range input provided is not correct! :: {e}')

    for part in outputs:
        result = []
        if not inv_choices == 'pairwise':
            output_answer = part.pop()
        else:
            output_answer = None
        if len(part) == 1 and isinstance(part, str):
            part = ''.join(part)
            if '-' in part:
                process_partitions(part)
                result.append(output_answer)
                process_output.append(result)
        else:  # Support multiple inputs but limited by BVA
            for choice in part:
                if isinstance(choice, str) and '-' in choice:
                    process_partitions(choice)
                else:
                    result.append(choice)
            result.append(output_answer)
            process_output.append(result)

    return process_output


def run(outputs: list, inv_choices: str) -> Optional[list]:
    copy_outputs = deepcopy(outputs)
    if not inv_choices == 'pairwise':
        for lst in copy_outputs:
            if len(lst) < 2:
                logger.critical('Did not provide all the inputs/answers for the function.')
                return

    return get_eq_partitions(copy_outputs, inv_choices)
