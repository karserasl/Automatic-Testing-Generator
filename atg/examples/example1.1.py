from techniques.pairwise import Pairwise

parameters = [
    ["Ford", "Volvo", "BMW"],
    [20000, 40000, 50000],
    ["New", "Used"],
    [0, 1, 2, 7, 8, 9],
    [0, 1, 2, 7, 8, 9]
    # ["Salaried", "Hourly", "Part-Time", "Contr."],
    # [6, 10, 15, 30, 60],
]
# sample parameters are is taken from
# http://www.stsc.hill.af.mil/consulting/sw_testing/improvement/cst.html

print("PAIRWISE:")
for i, pairs in enumerate(Pairwise(parameters)):
    print("{:2d}: {}".format(i, pairs))
