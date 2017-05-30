import unittest
import numpy as np
import flask
import json
from panoptes_aggregation import reducers


class TestProcessData(unittest.TestCase):
    def setUp(self):
        self.extracted_data = [
            {
                'T0_tool1_x': [1, 4],
                'T0_tool1_y': [2, 7],
                'T0_tool2_x': [3],
                'T0_tool2_y': [4]
            },
            {
                'T0_tool1_x': [1],
                'T0_tool1_y': [2]
            }
        ]

    def test_process_data(self):
        expected_result = {
            'T0_tool1': [(1, 2), (4, 7), (1, 2)],
            'T0_tool2': [(3, 4)]
        }
        self.assertDictEqual(reducers.cluster_points.process_data(self.extracted_data), expected_result)


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
        self.result = reducers.cluster_points.cluster_points(self.data_by_tool, eps=5, min_samples=3)
        self.expected = {
            'tool1_points_x': list(self.data_by_tool['tool1'][:, 0]),
            'tool1_points_y': list(self.data_by_tool['tool1'][:, 1]),
            'tool1_cluster_labels': [0] * c0_count + [1] * c1_count,
            'tool1_clusters_count': [c0_count, c1_count],
            'tool1_clusters_x': [c0_loc[0], c1_loc[0]],
            'tool1_clusters_y': [c0_loc[1], c1_loc[1]],
            'tool1_clusters_var_x': [c0_cov[0, 0], c1_cov[0, 0]],
            'tool1_clusters_var_y': [c0_cov[1, 1], c1_cov[1, 1]],
            'tool1_clusters_var_x_y': [c0_cov[0, 1], c1_cov[0, 1]],
        }

    def test_keys(self):
        for i in self.expected.keys():
            with self.subTest(i=i):
                self.assertIn(i, self.result)

    def test_cluster_values(self):
        for i in self.result.keys():
            with self.subTest(i=i):
                np.testing.assert_allclose(self.result[i], self.expected[i], atol=2)

    def test_type(self):
        for i in self.result.values():
            with self.subTest(i=i):
                self.assertIsInstance(i, list)


class TestReducerRequest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        request_data = json.dumps([
            {'data': {
                'T0_tool1_x': [1, 4],
                'T0_tool1_y': [2, 7],
                'T0_tool2_x': [3],
                'T0_tool2_y': [4]
            }},
            {'data': {
                'T0_tool1_x': [1],
                'T0_tool1_y': [2]
            }}
        ])
        self.request_kwargs = {
            'data': request_data,
            'content_type': 'application/json'
        }

    def test_process_request(self):
        expected = {
            'T0_tool1_points_x': [1, 4, 1],
            'T0_tool1_points_y': [2, 7, 2],
            'T0_tool1_cluster_labels': [-1, -1, -1],
            'T0_tool2_points_x': [3],
            'T0_tool2_points_y': [4],
            'T0_tool2_cluster_labels': [-1]
        }
        with self.app.test_request_context('/?eps=2', **self.request_kwargs):
            self.assertDictEqual(reducers.cluster_points.reducer_request(flask.request), expected)


if __name__ == '__main__':
    unittest.main()
