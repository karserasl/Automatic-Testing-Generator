def car_deals(brand: str, price: int = 4, cond: str = 'test3'):
    if brand == "Ford":
        if price <= 20000 and cond == "New":
            return "Good Deal"
        elif price >= 20000 and cond == 'Used':
            return 'Bad Deal'
        else:
            return 'Could be better'
    if brand == "BMW":
        if price >= 50000 and cond == "Used":
            return 'Bad Deal'
        elif price >= 40000 and (cond == 'New' or cond == 'Used'):
            return 'Could be better'
        else:
            return 'Good Deal'
    if brand == 'Volvo':
        if cond == 'New' and price < 40000:
            return 'Good Deal'
        else:
            return 'Could be better'


# import middleware.core
#
# a = middleware.core.ATG()
# a.analyse_file(
#     'C:/Users/Administrator/Uni-3rd_Year/CTEC3451 - Development Project/Development/Code/Automatic Testing Generator/mockapp/calculator.py')


from generator.generator import TestsGenerator

# print(run([['20-122', 'ghjhk'], [432,1234,432], ['4321','4321234','14123'], ['4321']]))
g = TestsGenerator()
p = {'Boundary_Value_Analysis': [], 'Equivalence_Partitioning': [[2147, 'dfas', 'fdsa'], ['fdsa', 'dfas', 'dfsa']]}
cls = 'Calculator'
f = 'uniClassification'
fil = 'C:/Users/Administrator/Uni-3rd_Year/CTEC3451 - Development Project/Development/Code/Automatic Testing Generator/mockapp/calculator.py'
a, c = g.dump(processed_output=p, filename=fil, cls=cls, method=f)
print(c)
