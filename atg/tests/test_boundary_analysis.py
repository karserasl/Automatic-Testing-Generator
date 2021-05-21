# @Author: Administrator
# @Date:   21/05/2021 06:20
import unittest
from unittest import mock
from unittest.mock import patch

from techniques.boundary_analysis import run


class Test(unittest.TestCase):
    def test_correct_inputs(self):
        inputs = [['0-39', 'Failed'], ['40-49', 'Pass'], ['50-59', '2:2'], ['60-69', '2:1'],
                  ['70-100', 'First!']]
        wrong_ans = 'Wrong Grade'
        expected = [[-1, 'Wrong Grade'], [0, 'Failed'], [1, 'Failed'], [38, 'Failed'], [39, 'Failed'], [40, 'Pass'],
                    [41, 'Pass'], [48, 'Pass'], [49, 'Pass'], [50, '2:2'], [51, '2:2'], [58, '2:2'], [59, '2:2'],
                    [60, '2:1'], [61, '2:1'], [68, '2:1'], [69, '2:1'], [70, 'First!'], [71, 'First!'], [99, 'First!'],
                    [100, 'First!']]
        self.assertEqual(
            run(outputs=inputs, inv_choices=wrong_ans),
            expected
        )

    @patch('logging.Logger.critical')
    def test_incorrect_inputs(self, mock):
        inputs = [['0-39', '40-49', 'Failed']]
        wrong_ans = 'Wrong Grade'
        expected = 'LIMITATION: Not able to process more than 1 BVA variable per function!'
        run(outputs=inputs, inv_choices=wrong_ans)
        mock.assert_called_with(expected)


if __name__ == '__main__':
    unittest.main()
