# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:36


class Calculator:

    def __init__(self):
        self.statement = "Completed init"

    def uniClassification(self, grade: int):
        """
        University grade calculator
        :param grade: grade of student
        :return: str
        """
        print(self.statement)

        if 0 <= grade < 39:
            return 'Failed'
        elif 40 <= grade < 50:
            return 'Pass'
        elif 50 <= grade < 60:
            return '2:2'
        elif 60 <= grade < 70:
            return '2:1'
        elif 70 <= grade <= 100:
            return 'First!'
        else:
            return 'Wrong grade.'

    @staticmethod
    def carDeals(brand: str, price: int = 4, cond: str = 'test3'):
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


def test(a: str, b: int) -> str:
    if a == 't' and 1 <= b <= 10:
        return 'inside'
    elif a == 'a' and 100 >= b >= 10:
        return 'test'

    if b > 10:
        return 'int'
    if a == 't':
        return 'single'
    elif a == 'a':
        return 'hey'

    return 'error'
