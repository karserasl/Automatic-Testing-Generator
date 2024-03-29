# @Author: Administrator
# @Date:   03/02/2021 14:26

# sample parameters are is taken from
# http://www.stsc.hill.af.mil/consulting/sw_testing/improvement/cst.html
from techniques.pairwise import Pairwise

parameters = [
    ["Ford", "Volvo", "BMW"],
    [20000, 40000, 50000],
    ["New", "Used", "test"],
    # [0, 1, 2, 7, 8, 9],
    # [0],
    # ["Salaried"],
    # [6],
]

print("PAIRWISE:")
for i, pairs in enumerate(Pairwise(parameters)):
    print("{:2d}: {}".format(i, pairs))
