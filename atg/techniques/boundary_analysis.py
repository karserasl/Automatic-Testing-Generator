# @Author: Administrator
# @Date:   03/02/2021 14:26
import sys
import logging
from typing import Optional
from copy import deepcopy
logger = logging.getLogger(__name__)

TECH_ID = 'Boundary_Value_Analysis'

MODULE_NAME = sys.modules[__name__].__name__.split('.')[-1]
PACKAGE_NAME = sys.modules[__name__].__name__.split('.')[-2]


def get_index(ls, elem):
    # Function to get the index which match the criteria.
    for index, lst in enumerate(ls):
        for item in lst:
            if item == elem:
                # The criteria matches, return the indexes.
                return index


def get_boundaries(outputs: list, inv_choices: str) -> list:
    """
    Returning a list of lists with each list containing the inputs and the last item in the list is the expected output.
    :param outputs: list of inputs from GUI
    :param inv_choices: the output if out-of-bounds
    :return: list of lists
    """
    process_output = []

    def process_partition(partition):
        boundaries = set()
        if '-' in partition:
            p = list(map(int, partition.split('-')))
            boundaries.update({p[0] - 1, p[0], p[0] + 1, p[1] - 1, p[1], p[1] + 1})

            sort_bounds = sorted(boundaries)
            inv_min_bound = [sort_bounds.pop(0), inv_choices]
            inv_max_bound = [sort_bounds.pop(), inv_choices]
            # Since it is sorted and starting from the lowest, only the lowest value need to be checked.
            if not any(inv_min_bound[0] in sublist for sublist in process_output):
                process_output.extend([inv_min_bound, inv_max_bound])
            # Check if overlapping and if it is, check the answer (last item) and replace it if had the invalid choice.
            for i in sort_bounds:
                if any(i in sublist for sublist in process_output):
                    ind = get_index(process_output, i)
                    ans = process_output[ind][-1]
                    if ans == inv_choices:
                        process_output.pop(ind)

                process_output.append([i, output_answer])

    for part in outputs:
        output_answer = part.pop()
        if len(part) == 1 and isinstance(part, list):

            part = ''.join([p for p in part if isinstance(p, str)])
            process_partition(part)
        else:
            logger.critical('LIMITATION: Not able to process more than 1 BVA variable per function!')
            break
    print(process_output)
    return process_output


def run(outputs: list, inv_choices: str) -> Optional[list]:
    print(outputs, inv_choices)
    copy_outputs = deepcopy(outputs)
    for lst in copy_outputs:
        if len(lst) < 2:
            logger.critical('Did not provide all the inputs/answers for the function.')
            return

    return get_boundaries(copy_outputs, inv_choices)
