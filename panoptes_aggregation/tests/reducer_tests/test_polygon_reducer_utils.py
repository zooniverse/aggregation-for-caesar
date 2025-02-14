import unittest
import numpy as np
import shapely
from panoptes_aggregation.reducers import polygon_reducer_utils as utils
from pandas._libs.tslibs.timestamps import Timestamp as pdtimestamp
import datetime


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

    def test_IoU_metric_polygon_self_intersection(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0], [-0.5, 0.2]]))
        a = [0, 0]
        b = [1, 1]
        data_in = [{'polygon': square1}, {'polygon': square2}]
        expected = 1.
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

    def test_IoU_distance_matrix_of_cluster(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0, 2], [0, 3], [1, 3], [1, 2]]))
        square4 = shapely.Polygon(np.array([[-2.0, 0.5], [-1., 0.5], [-1., 1.5], [-2.0, 1.5]]))
        square5 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))
        
        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3},
                {'polygon': square4},
                {'polygon': square5}]
        X = np.array([[0, 0], [1,1], [2,2], [3,3], [4,4]])
        cdx = np.array([True, True, False, False, True])
        result = utils.IoU_distance_matrix_of_cluster(cdx, X, data)
        expected = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        differance = np.abs(result - expected).flatten()
        # Want it to be within this error
        self.assertTrue(all(differance<0.001))

    def test_IoU_cluster_mean_distance(self):
        distances_matrix = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        result = utils.IoU_cluster_mean_distance(distances_matrix)
        expected = 0.7301587333333334
        differance = np.abs(result - expected)
        self.assertTrue(differance<0.00001)

    def test_IoU_cluster_mean_distance_same_user(self):
        distances_matrix = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., np.inf],
                            [0.66666667, np.inf, 0.]])
        result = utils.IoU_cluster_mean_distance(distances_matrix)
        expected = 0.7777777800000001
        differance = np.abs(result - expected)
        self.assertTrue(differance<0.00001)

    def test_cluster_average_last_str_format(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC']
        expected = square1
        result = utils.cluster_average_last(data, created_at=created_at_list)
        self.assertEqual(result, expected)

    def test_cluster_average_last_pd_format(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = [pdtimestamp('2025-01-21 10:46:23'),
                           pdtimestamp('2025-01-21 10:46:21'),
                           pdtimestamp('2025-01-21 10:46:22')]
        expected = square1
        result = utils.cluster_average_last(data, created_at=created_at_list)
        self.assertEqual(result, expected)

    def test_cluster_average_last_timdate_format(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = [datetime.datetime.strptime('2025-01-21 10:46:23', "%Y-%m-%d %H:%M:%S"),
                           datetime.datetime.strptime('2025-01-21 10:46:21', "%Y-%m-%d %H:%M:%S"),
                           datetime.datetime.strptime('2025-01-21 10:46:22', "%Y-%m-%d %H:%M:%S")]
        kwargs = {'created_at': created_at_list}
        expected = square1
        result = utils.cluster_average_last(data, **kwargs)
        self.assertEqual(result, expected)

    def test_cluster_average_median(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        distance_matrix =  np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        kwargs = {'distance_matrix': distance_matrix}
        expected = square1
        result = utils.cluster_average_median(data, **kwargs)
        self.assertEqual(result, expected)


    def test_cluster_average_median_same_user(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        distance_matrix =  np.array([[0., np.inf, 0.66666667],
                            [ np.inf, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        kwargs = {'distance_matrix': distance_matrix}
        expected = square3
        result = utils.cluster_average_median(data, **kwargs)
        self.assertEqual(result, expected)

    def test_cluster_average_intersection(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC']
        kwargs = {'created_at': created_at_list}
        expected = shapely.Polygon(np.array([[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0], [0.5, 0.5]]))
        result = utils.cluster_average_intersection(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_one_object(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1, 'time': 100.3}]
        created_at_list = ['2025-01-21 10:46:23 UTC']
        kwargs = {'created_at': created_at_list}
        expected = square1
        result = utils.cluster_average_intersection(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_n_polygons_one_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))
        square4 = shapely.Polygon(np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3},
                {'polygon': square4}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC',
                           '2025-01-21 10:46:26 UTC']
        kwargs = {'n_polygons': 1}
        expected = shapely.Polygon(np.array([[1.5, 0.5],
                                             [1.5, 0. ],
                                             [1., 0. ],
                                             [0.5, 0. ],
                                             [0., 0. ],
                                             [0., 0.5],
                                             [0., 1. ],
                                             [0., 1.5],
                                             [0.5, 1.5],
                                             [1., 1.5],
                                             [1.5, 1.5],
                                             [1.5, 1. ],
                                             [1.5, 0.5]]))
        result = utils.cluster_average_intersection_n_polygons(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_n_polygons_two_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))
        square4 = shapely.Polygon(np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3},
                {'polygon': square4}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC',
                           '2025-01-21 10:46:26 UTC']
        kwargs = {'n_polygons': 2}
        expected = shapely.Polygon(np.array([[0., 0.5],
                                             [0., 1. ],
                                             [0.5, 1. ],
                                             [0.5, 1.5],
                                             [1., 1.5],
                                             [1., 1. ],
                                             [1.5, 1. ],
                                             [1.5, 0.5],
                                             [1., 0.5],
                                             [1., 0. ],
                                             [0.5, 0. ],
                                             [0.5, 0.5],
                                             [0., 0.5]]))
        result = utils.cluster_average_intersection_n_polygons(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_n_polygons_four_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))
        square4 = shapely.Polygon(np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3},
                {'polygon': square4}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC',
                           '2025-01-21 10:46:26 UTC']
        kwargs = {'n_polygons': 4}
        expected = shapely.Polygon(np.array([[0.5, 0.5],
                                             [0.5, 1. ],
                                             [1., 1. ],
                                             [1., 0.5],
                                             [0.5, 0.5]]))
        result = utils.cluster_average_intersection_n_polygons(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_intersection_n_polygons_five_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))
        square4 = shapely.Polygon(np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3},
                {'polygon': square4}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC',
                           '2025-01-21 10:46:26 UTC']
        kwargs = {'n_polygons': 5}
        expected = []
        result = utils.cluster_average_intersection_n_polygons(data, **kwargs)
        self.assertTrue(expected==result)

    def test_cluster_average_union(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC']
        kwargs = {'created_at': created_at_list}
        expected = shapely.Polygon(np.array([[0.0, 0.0], [1.5, 0.0], [1.5, 1.0], [1.0, 1.0], [1.0, 1.5], [0.0, 1.5]]))
        result = utils.cluster_average_union(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))

    def test_cluster_average_union_one_object(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1}]
        created_at_list = ['2025-01-21 10:46:23 UTC']
        kwargs = {'created_at': created_at_list}
        expected = square1
        result = utils.cluster_average_union(data, **kwargs)
        self.assertTrue(shapely.equals(result, expected))
