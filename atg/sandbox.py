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


from techniques.equivalance_partitioning import run
print(run([['20-16', 'ghjhk']], 'Wrong'))
