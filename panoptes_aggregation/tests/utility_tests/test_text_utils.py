import unittest
import numpy as np
from panoptes_aggregation.reducers import text_utils


theta_1 = [
    180,
    179,
    45,
    -90,
    135
]

theta_2 = [
    -180,
    -179,
    135,
    135,
    -135
]

delta_theta = [
    0,
    2,
    90,
    135,
    90
]

theta_lists = [
    np.array([179, -179]),
    np.array([45, -45]),
    np.array([-135, -45]),
    np.array([135, 45])
]

theta_avg = [
    180,
    0,
    -90,
    90
]


class TestTextUtils(unittest.TestCase):
    def test_angle_metric(self):
        '''Test the angle metric'''
        for i in range(len(theta_1)):
            with self.subTest(i=i):
                result = text_utils.angle_metric(theta_1[i], theta_2[i])
                self.assertEqual(result, delta_theta[i])

    def test_avg_angle(self):
        '''Test average angle'''
        for i in range(len(theta_lists)):
            with self.subTest(i=i):
                result = text_utils.avg_angle(theta_lists[i])
                self.assertEqual(result, theta_avg[i])

    def test_empty_gutter(self):
        '''Test empty list passed into gutter'''
        result = text_utils.gutter([])
        np.testing.assert_equal(result, np.array([]))

    def test_no_consensus(self):
        '''Test empty list passed into consensus_score'''
        result = text_utils.consensus_score([])
        self.assertEqual(result, 0.0)

    def test_bad_keyword(self):
        '''Test error is raised if a bad keyword is used for dot_freq'''
        with self.assertRaises(ValueError):
            text_utils.cluster_by_line(
                [],
                [],
                [],
                [],
                {'dot_freq': 'bad_keyword'},
                {}
            )


if __name__ == '__main__':
    unittest.main()
