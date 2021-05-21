# @Author: Administrator
# @Date:   21/05/2021 07:44
from unittest import TestCase
import unittest
from unittest.mock import patch

from techniques.equivalance_partitioning import run


class Test(unittest.TestCase):
    def test_correct_inputs(self):
        inputs = [['0-39', 'Failed'], ['40-49', 'Pass'], ['50-59', '2:2'], ['60-69', '2:1'],
                  ['70-100', 'First!']]
        wrong_ans = 'Wrong Grade'

        fun = [i[0] for i in run(outputs=inputs, inv_choices=wrong_ans)]
        self.assertTrue(
            [i for i in fun if str(i).isdigit()]
        )

    @patch('logging.Logger.critical')
    def test_len(self, mock):
        inputs = [['0-39'], ['40-49'], ['50-59', '2:2'], ['60-69', '2:1'],
                  ['70-100', 'First!']]
        expected = 'Did not provide all the inputs/answers for the function.'
        run(outputs=inputs, inv_choices='')
        mock.assert_called_with(expected)


if __name__ == '__main__':
    unittest.main()
