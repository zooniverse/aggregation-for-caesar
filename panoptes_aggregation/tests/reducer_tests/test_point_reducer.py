import unittest
import numpy as np
import flask
import json
from panoptes_aggregation.reducers.point_reducer import process_data, point_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

c0_cov = np.array([[3, 0.5], [0.5, 4]])
c1_cov = np.array([[7, -0.5], [-0.5, 5]])
c0_loc = np.array([12, 15])
c1_loc = np.array([20, 25])
c0_count = 15
c1_count = 8
np.random.seed(5000)
xy = np.vstack([
    np.random.multivariate_normal(c0_loc, c0_cov, size=c0_count),
    np.random.multivariate_normal(c1_loc, c1_cov, size=c1_count)
])
extracted_data = [
    {
        'tool1_x': list(xy[:12, 0]),
        'tool1_y': list(xy[:12, 1]),
        'tool2_x': [3],
        'tool2_y': [4]
    },
    {
        'tool1_x': list(xy[12:, 0]),
        'tool1_y': list(xy[12:, 1]),
    }
]
processed_data = {
    'tool1': [tuple(z) for z in list(xy)],
    'tool2': [(3, 4)]
}
reduced_data = {
    'tool1_points_x': list(xy[:, 0]),
    'tool1_points_y': list(xy[:, 1]),
    'tool1_cluster_labels': [0] * c0_count + [1] * c1_count,
    'tool1_clusters_count': [c0_count, c1_count],
    'tool1_clusters_x': [c0_loc[0], c1_loc[0]],
    'tool1_clusters_y': [c0_loc[1], c1_loc[1]],
    'tool1_clusters_var_x': [c0_cov[0, 0], c1_cov[0, 0]],
    'tool1_clusters_var_y': [c0_cov[1, 1], c1_cov[1, 1]],
    'tool1_clusters_var_x_y': [c0_cov[0, 1], c1_cov[0, 1]],
    'tool2_points_x': [3],
    'tool2_points_y': [4],
    'tool2_cluster_labels': [-1]
}


class TestClusterPoints(unittest.TestCase):
    def test_process_data(self):
        result = process_data(extracted_data)
        self.assertDictEqual(result, processed_data)

    def test_keys(self):
        result = point_reducer(extracted_data, eps=5, min_samples=3)
        for i in reduced_data.keys():
            with self.subTest(i=i):
                self.assertIn(i, result)

    def test_cluster_values(self):
        result = point_reducer._original(processed_data, eps=5, min_samples=3)
        for i in result.keys():
            with self.subTest(i=i):
                np.testing.assert_allclose(result[i], reduced_data[i], atol=2)

    def test_type(self):
        result = point_reducer._original(processed_data, eps=5, min_samples=3)
        for i in result.values():
            with self.subTest(i=i):
                self.assertIsInstance(i, list)

    def test_point_reducer(self):
        result = point_reducer(extracted_data, eps=5, min_samples=3)
        for i in result.keys():
            with self.subTest(i=i):
                np.testing.assert_allclose(result[i], reduced_data[i], atol=2)

    def test_process_request(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }
        with app.test_request_context('/?eps=5&min_samples=3', **request_kwargs):
            result = point_reducer(flask.request)
            for i in result.keys():
                with self.subTest(i=i):
                    np.testing.assert_allclose(result[i], reduced_data[i], atol=2)


if __name__ == '__main__':
    unittest.main()
