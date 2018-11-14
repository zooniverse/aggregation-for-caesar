import unittest
from panoptes_aggregation.reducers.shape_metric import avg_angle

test_angle_factor_1 = [
    [1, 359],
    [179, -179],
    [1, 179],
    [-1, -179],
    [90, 0, 0],
    [450, 0, 360]
]

expected_angle_avg_factor_1 = [
    0,
    180,
    90,
    270,
    30,
    30
]

test_angle_factor_2 = [
    [1, 179],
    [0, 45, 90],
    [45, 135, 0]
]

expected_angle_avg_factor_2 = [
    0,
    45,
    0
]

test_angle_factor_3 = [
    [1, 119],
    [0, 44, 45, 46, 90],
    [30, 90],
    [150, 90],
    [30, 90, 0],
    [45, 165, 285]
]

expected_angle_avg_factor_3 = [
    0,
    45,
    60,
    60,
    0,
    45
]


class AvgAngle(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def avgCheck(self, test, expected, factor=1):
        for i, j in zip(test, expected):
            with self.subTest(i=i):
                result = avg_angle(i, factor=factor)
                self.assertEqual(result, j)

    def testFactor1(self):
        '''Test average angle with factor=1'''
        self.avgCheck(
            test_angle_factor_1,
            expected_angle_avg_factor_1,
            factor=1
        )

    def testFactor2(self):
        '''Test average angle with factor=2'''
        self.avgCheck(
            test_angle_factor_2,
            expected_angle_avg_factor_2,
            factor=2
        )

    def testFactor3(self):
        '''Test average angle with factor=3'''
        self.avgCheck(
            test_angle_factor_3,
            expected_angle_avg_factor_3,
            factor=3
        )
