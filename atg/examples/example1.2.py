# @Author: Administrator
# @Date:   03/02/2021 14:26

# sample parameters are is taken from
# http://www.stsc.hill.af.mil/consulting/sw_testing/improvement/cst.html
from techniques.pairwise import Pairwise


parameters = [
    ["Brand X", "Brand Y"],
    ["98", "NT", "2000", "XP"],
    ["Internal", "Modem"],
    ["Salaried", "Hourly", "Part-Time", "Contr."],
    [6, 10, 15, 30, 60],
]

print("TRIPLEWISE:")
for i, pairs in enumerate(Pairwise(parameters, n=3)):
    print("{:2d}: {}".format(i, pairs))
