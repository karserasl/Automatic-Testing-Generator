from __future__ import absolute_import

import logging
import sys
from collections import namedtuple
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import combinations
from techniques.equivalance_partitioning import run as eqv_run

logger = logging.getLogger(__name__)

TECH_ID = 'Pairwise'

MODULE_NAME = sys.modules[__name__].__name__.split('.')[-1]
PACKAGE_NAME = sys.modules[__name__].__name__.split('.')[-2]


def run(outputs: list) -> list:
    copy_outputs = deepcopy(outputs)
    process_output = []
    if any('-' in x for j in copy_outputs for x in j):
        eqv_output = eqv_run(copy_outputs, 'Pairwise')
        copy_outputs = [[elem for elem in sublist if elem is not None] for sublist in eqv_output]
    for i, pairs in enumerate(Pairwise(copy_outputs)):
        process_output.append(pairs)
    return process_output


def max_comb_number(matrix, n):
    """
    Get the maximum number of combinations possible
    :param matrix: list of lists
    :param n: tuples length to create
    :return: the sum of reduced combination numbers
    ``Example``
        >>> combinations([0,1,2], 2) == [(0, 1), (0, 2), (1, 2)]
        for every i in combinations, x * y
        sum the list.
    """
    list_param_length = [len(lst) for lst in matrix]
    return sum([reduce(lambda x, y: x * y, i) for i in combinations(list_param_length, n)])


def cmp_item(lhs, rhs):
    if lhs.weights == rhs.weights:
        return 0

    return -1 if lhs.weights < rhs.weights else 1


class Pairwise:
    def __init__(self, parameters, filter_func=lambda x: True, previously_tested=None, n=2):
        if not previously_tested:
            previously_tested = [[]]
        self._outputs = parameters
        self._validate_parameter(parameters)
        self._param_name_list = []
        # https://realpython.com/python-namedtuple/
        self._pairs_class = namedtuple("Pairs", self._param_name_list)
        self._filter_func = filter_func
        self._n = n
        self._pairs = CombinationStorage(n)
        self._max_combinations_unique = max_comb_number(parameters, n)
        self._working_item_matrix = self._get_working_item_matrix(parameters)
        for arr in previously_tested:
            if not arr:
                continue
            if len(arr) != len(self._working_item_matrix):
                logger.error("previously tested combination is not complete")
            if not self._filter_func(arr):
                logger.error("invalid tested combination is provided")
            tested = []
            for i, val in enumerate(arr):
                idxs = [Element(item.id, 0) for item in self._working_item_matrix[i] if item.value == val]
                if len(idxs) != 1:
                    logger.error(
                        "value from previously tested combination is not found in the parameters or found more than "
                        "once"
                    )

                tested.append(idxs[0])

            self._pairs.add_sequence(tested)

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        assert len(self._pairs) <= self._max_combinations_unique

        if len(self._pairs) == self._max_combinations_unique:
            # no reasons to search further - all pairs are found
            raise StopIteration()

        previous_unique_pairs_count = len(self._pairs)
        chosen_item_list = [None] * len(self._working_item_matrix)
        indexes = [None] * len(self._working_item_matrix)

        direction = 1
        i = 0

        while -1 < i < len(self._working_item_matrix):
            if direction == 1:
                # move forward
                self._resort_working_array(chosen_item_list[:i], i)
                indexes[i] = 0
            elif direction == 0 or direction == -1:
                # scan current array or go back
                indexes[i] += 1
                if indexes[i] >= len(self._working_item_matrix[i]):
                    direction = -1
                    if i == 0:
                        raise StopIteration()
                    i += direction
                    continue
                direction = 0
            else:
                logger.error(f"next(): unknown 'direction' code '{direction}'")

            chosen_item_list[i] = self._working_item_matrix[i][indexes[i]]

            if self._filter_func(self._get_values(chosen_item_list[: i + 1])):
                assert direction > -1
                direction = 1
            else:
                direction = 0
            i += direction

        if len(self._working_item_matrix) != len(chosen_item_list):
            raise StopIteration()

        self._pairs.add_sequence(chosen_item_list)

        if len(self._pairs) == previous_unique_pairs_count:
            # could not find new unique pairs - stop
            raise StopIteration()

        # replace returned array elements with real values and return it
        return self._get_iteration_value(chosen_item_list)

    @staticmethod
    def _validate_parameter(value):
        if len(value) < 2:
            logger.error("must provide more than one option")

        for parameter_list in value:
            if not parameter_list:
                logger.error("each parameter arrays must have at least one item")

    def _resort_working_array(self, chosen_item_list, num):
        for item in self._working_item_matrix[num]:
            data_node = self._pairs.get_node_info(item)

            new_combs = [
                # numbers of new combinations to be created if this item is
                # appended to array
                {key(z) for z in combinations(chosen_item_list + [item], i + 1)}
                - self._pairs.get_combs()[i]
                for i in range(0, self._n)
            ]

            # weighting the node node that creates most of new pairs is the best
            weights = [-len(new_combs[-1])]

            # less used outbound connections most likely to produce more new
            # pairs while search continues
            weights.extend(
                [len(data_node.outbound)]
                + [len(x) for x in reversed(new_combs[:-1])]
                + [-data_node.counter]  # less used node is better
            )

            # otherwise we will prefer node with most of free inbound
            # connections; somehow it works out better ;)
            weights.append(-len(data_node.inside))

            item.set_elem_weights(weights)

        self._working_item_matrix[num].sort(key=cmp_to_key(cmp_item))

    @staticmethod
    def _get_working_item_matrix(matrix):
        return [
            [Element(f"a{lst_index}v{value_index}", value_str) for value_index, value_str in enumerate(lst)]
            for lst_index, lst in enumerate(matrix)
        ]

    @staticmethod
    def _get_values(item_list):
        return [item.value for item in item_list]

    def _get_iteration_value(self, item_list):
        if not self._param_name_list:
            return [item.value for item in item_list]

        return self._pairs_class(*[item.value for item in item_list])


class Element:
    @property
    def id(self):
        return self._item_id

    @property
    def value(self):
        return self._value

    def __init__(self, item_id, value):
        self._weights = None
        self._item_id = item_id
        self._value = value

    def __str__(self):
        return str(self.__dict__)

    @property
    def weights(self):
        return self._weights

    def set_elem_weights(self, elem_weights):
        self._weights = elem_weights


class Node:
    @property
    def id(self):
        return self._node_id

    @property
    def counter(self):
        return self._counter

    def __init__(self, node_id):
        self._node_id = node_id
        self._counter = 0
        self.inside = set()
        self.outbound = set()

    def __str__(self):
        return str(self.__dict__)

    def inc_counter(self):
        self._counter += 1


key_cache = {}


def key(items):
    if items in key_cache:
        return key_cache[items]

    key_value = tuple([x.id for x in items])
    key_cache[items] = key_value

    return key_value


class CombinationStorage:
    def __init__(self, n):
        self._n = n
        self._nodes = {}
        self._array_of_combinations = [set() for _ in range(n)]

    def __len__(self):
        return len(self._array_of_combinations[-1])

    def add_sequence(self, sequence):
        for i in range(1, self._n + 1):
            for combination in combinations(sequence, i):
                self.__add_combination(combination)

    def get_node_info(self, item):
        return self._nodes.get(item.id, Node(item.id))

    def get_combs(self):
        return self._array_of_combinations

    def __add_combination(self, combination):
        n = len(combination)
        assert n > 0

        self._array_of_combinations[n - 1].add(key(combination))
        if n == 1 and combination[0].id not in self._nodes:
            self._nodes[combination[0].id] = Node(combination[0].id)
            return

        ids = [x.id for x in combination]
        for i, id in enumerate(ids):
            curr = self._nodes[id]
            curr.inc_counter()
            curr.inside.update(ids[:i])
            curr.outbound.update(ids[i + 1:])
