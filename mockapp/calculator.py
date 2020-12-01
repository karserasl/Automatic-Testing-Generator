# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:36

class Calculator:
    @staticmethod
    def add(a: int, b: int) -> int:
        """
        Adding numbers
        :param a: Number 1
        :param b: Number 2
        :return: Result of addition
        :eq: 4-35
        """
        return a + b

    @staticmethod
    def uniClassification(a: int) -> None:
        """
        University grade calculator
        :param a: grade of student
        :return: str
        :eq: 0-39: 'Failed', 40-100: 'Pass', 'Wrong grade.'
        """
        # if 0 <= a < 30:
        #     print('Failed')
        # elif 30 <= a < 40:
        #     print('Retry')
        # elif 40 <= a < 50:
        #     print('Pass')
        # elif 50 <= a < 60:
        #     print('2:2')
        # elif 60 <= a < 70:
        #     print('2:1')
        # elif 70 <= a <= 100:
        #     print('First!')
        if 0 <= a < 40:
            print('Failed')
        elif 40 <= a <= 100:
            print('Pass')
        else:
            print('Wrong grade.')
