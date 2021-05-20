#!/usr/bin/env python3

from collections import OrderedDict

from techniques.pairwise import Pairwise


parameters = OrderedDict(
    {"brand": ["Brand X", "Brand Y"], "os": ["98", "NT", "2000", "XP"], "minute": [15, 30, 60]}
)

# parameters = OrderedDict(
#     {"a": ["Brand 1", "Brand 2"], "b": ["b_test1", "b_test2", "b_test3"], "c": ['c_test1', 'c_test2']}
# )

print("PAIRWISE:")
print(f'Inputs: {parameters} \n')
for i, pairs in enumerate(Pairwise(parameters)):
    print("{:2d}: {}".format(i, pairs))
