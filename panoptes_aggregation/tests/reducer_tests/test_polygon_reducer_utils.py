import unittest
import numpy as np
import shapely
from panoptes_aggregation.reducers import polygon_reducer_utils as utils


class TestIoUMetric(unittest.TestCase):

    def test_IoU_metric_polygon_no_overlap(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[2, 2], [2, 3], [3, 3], [3, 2]]))
        a = [0, 0]
        b = [1, 1]
        data_in = [{'polygon': square1}, {'polygon': square2}]
        expected = 1.0
        result = utils.IoU_metric_polygon(a, b, data_in=data_in)
        self.assertEqual(result, expected)

    def test_IoU_metric_polygon_overlap(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        a = [0, 0]
        b = [1, 1]
        data_in = [{'polygon': square1}, {'polygon': square2}]
        expected = 1 - 0.3333333333333333
        result = utils.IoU_metric_polygon(a, b, data_in=data_in)
        self.assertEqual(result, expected)

    def test_IoU_metric_polygon_same_polygon(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        a = [0, 0]
        b = [0, 1]
        data_in = [{'polygon': square1}, {'polygon': square2}]
        expected = 0.
        result = utils.IoU_metric_polygon(a, b, data_in=data_in)
        self.assertEqual(result, expected)

    def test_IoU_metric_polygon_same_user(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        a = [0, 0]
        b = [1, 0]
        data_in = [{'polygon': square1}, {'polygon': square2}]
        expected = np.inf
        result = utils.IoU_metric_polygon(a, b, data_in=data_in)
        self.assertEqual(result, expected)

    def test_cluster_average_last(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1, 'time': 100.3},
                {'polygon': square2, 'time': 100.1},
                {'polygon': square3, 'time': 100.2}]
        expected = square1
        result = utils.cluster_average_last(data)
        self.assertEqual(result, expected)

    def test_cluster_average_intersection(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1, 'time': 100.3},
                {'polygon': square2, 'time': 100.1},
                {'polygon': square3, 'time': 100.2}]
        expected = shapely.Polygon(np.array([[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0], [0.5, 0.5]]))
        result = utils.cluster_average_intersection(data)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_one_object(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1, 'time': 100.3}]
        expected = square1
        result = utils.cluster_average_intersection(data)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_union(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1, 'time': 100.3},
                {'polygon': square2, 'time': 100.1},
                {'polygon': square3, 'time': 100.2}]
        expected = shapely.Polygon(np.array([[0.0, 0.0], [1.5, 0.0], [1.5, 1.0], [1.0, 1.0], [1.0, 1.5], [0.0, 1.5]]))
        result = utils.cluster_average_union(data)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_union_one_object(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1, 'time': 100.3}]
        expected = square1
        result = utils.cluster_average_union(data)
        self.assertTrue(shapely.equals(result, expected))
