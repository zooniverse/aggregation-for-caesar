import unittest
import numpy as np
import reducers.cluster_points as cp


class TestProcessData(unittest.TestCase):
    def setUp(self):
        self.extracted_data = [
            {
                'tool1_x': 1,
                'tool1_y': 2,
                'tool2_x': 3,
                'tool2_y': 4
            },
            {
                'tool1_x': 1,
                'tool1_y': 2
            }
        ]

    def test_process_data(self):
        expected_result = {
            'tool1': [[1, 2], [1, 2]],
            'tool2': [[3, 4]]
        }
        self.assertEqual(cp.process_data(self.extracted_data), expected_result)


class TestClusterPoints(unittest.TestCase):
    def setUp(self):
        self.c0_cov = np.array([[3, 0.5], [0.5, 4]])
        self.c1_cov = np.array([[7, -0.5], [-0.5, 5]])
        self.c0_loc = np.array([12, 15])
        self.c1_loc = np.array([20, 25])
        self.c0_count = 15
        self.c1_count = 8
        np.random.seed(5000)
        self.data_by_tool = {
            'tool1': np.vstack([
                np.random.multivariate_normal(self.c0_loc, self.c0_cov, size=self.c0_count),
                np.random.multivariate_normal(self.c1_loc, self.c1_cov, size=self.c1_count)
            ])
        }
        self.result = cp.cluster_points(self.data_by_tool)

    def test_number_clusters(self):
        self.assertEqual(len(self.result), 12)

    def test_cluster_count(self):
        self.assertEqual(self.result['tool1_cluster0_count'], self.c0_count)
        self.assertEqual(self.result['tool1_cluster1_count'], self.c1_count)

    def test_cluster_loc(self):
        # since we are dealing with small numbers of data points atol is large
        np.testing.assert_allclose(self.result['tool1_cluster0_x'], self.c0_loc[0], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster0_y'], self.c0_loc[1], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster1_x'], self.c1_loc[0], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster1_y'], self.c1_loc[1], atol=2)

    def test_cluster_cov(self):
        # since we are dealing with small numbers of data points atol is large
        np.testing.assert_allclose(self.result['tool1_cluster0_var_x'], self.c0_cov[0, 0], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster0_var_y'], self.c0_cov[1, 1], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster0_var_x_y'], self.c0_cov[0, 1], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster1_var_x'], self.c1_cov[0, 0], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster1_var_y'], self.c1_cov[1, 1], atol=2)
        np.testing.assert_allclose(self.result['tool1_cluster1_var_x_y'], self.c1_cov[0, 1], atol=2)
