import unittest
import numpy as np
import flask
import json
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
        c0_cov = np.array([[3, 0.5], [0.5, 4]])
        c1_cov = np.array([[7, -0.5], [-0.5, 5]])
        c0_loc = np.array([12, 15])
        c1_loc = np.array([20, 25])
        c0_count = 15
        c1_count = 8
        np.random.seed(5000)
        self.data_by_tool = {
            'tool1': np.vstack([
                np.random.multivariate_normal(c0_loc, c0_cov, size=c0_count),
                np.random.multivariate_normal(c1_loc, c1_cov, size=c1_count)
            ])
        }
        self.result = cp.cluster_points(self.data_by_tool, eps=5, min_samples=3)
        self.expected = {
            'tool1_cluster0_count': c0_count,
            'tool1_cluster0_x': c0_loc[0],
            'tool1_cluster0_y': c0_loc[1],
            'tool1_cluster0_var_x': c0_cov[0, 0],
            'tool1_cluster0_var_y': c0_cov[1, 1],
            'tool1_cluster0_var_x_y': c0_cov[0, 1],
            'tool1_cluster1_count': c1_count,
            'tool1_cluster1_x': c1_loc[0],
            'tool1_cluster1_y': c1_loc[1],
            'tool1_cluster1_var_x': c1_cov[0, 0],
            'tool1_cluster1_var_y': c1_cov[1, 1],
            'tool1_cluster1_var_x_y': c1_cov[0, 1]
        }

    def test_keys(self):
        for i in self.expected.keys():
            with self.subTest(i=i):
                self.assertIn(i, self.result)

    def test_cluster_values(self):
        for i in self.result.keys():
            with self.subTest(i=i):
                self.assertAlmostEqual(self.result[i], self.expected[i], delta=2)


class TestProcessRequest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        request_data = json.dumps([
            {
                'tool1_x': 1,
                'tool1_y': 2,
                'tool2_x': 3,
                'tool2_y': 4
            },
            {
                'tool1_x': 5,
                'tool1_y': 6
            }
        ])
        self.request_kwargs = {
            'data': request_data,
            'content_type': 'application/json'
        }

    def test_process_request(self):
        with self.app.test_request_context('/?eps=2', **self.request_kwargs):
            self.assertDictEqual(cp.process_request(flask.request), {})


if __name__ == '__main__':
    unittest.main()
