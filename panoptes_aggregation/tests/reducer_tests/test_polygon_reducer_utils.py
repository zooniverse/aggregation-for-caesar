import unittest
import numpy as np
import shapely
from panoptes_aggregation.reducers import polygon_reducer_utils as utils
from pandas._libs.tslibs.timestamps import Timestamp as pdtimestamp
import datetime


class TestIoUMetric(unittest.TestCase):

    def test__polygons_unify(self):
        shape1 = shapely.Polygon(np.array([[0, 0], [0, 3], [1, 3], [1, 0]]))
        shape2 = shapely.Polygon(np.array([[2, 0], [2, 3], [3, 3], [3, 0]]))
        shape3 = shapely.Polygon(np.array([[0, 2], [0, 3], [3, 3], [3, 2]]))
        shape4 = shapely.Polygon(np.array([[0, 0], [0, 1], [3, 1], [3, 0]]))

        # make a large square with a whole in the centre
        polygons = [shape1, shape2, shape3, shape4]
        # Should return a square with no hole
        expected = shapely.Polygon(np.array([[0, 0], [0, 3], [3, 3], [3, 0]]))
        result = utils._polygons_unify(polygons)
        self.assertTrue(shapely.equals(result, expected))

    def test__polygons_unify_non_polygons(self):
        shape1 = shapely.Polygon(np.array([[0, 0], [0, 3], [1, 3], [1, 0]]))
        shape2 = shapely.Polygon(np.array([[2, 0], [2, 3], [3, 3], [3, 0]]))
        shape3 = shapely.Polygon(np.array([[0, 2], [0, 3], [3, 3], [3, 2]]))
        shape4 = shapely.Polygon(np.array([[0, 0], [0, 1], [3, 1], [3, 0]]))
        shape5 = shapely.LineString([(0, -1), (0, 1)])

        # make a large square with a whole in the centre
        polygons = [shape1, shape2, shape3, shape4, shape5]
        # Should return a square with no hole
        expected = shapely.Polygon(np.array([[0, 0], [0, 3], [3, 3], [3, 0]]))
        result = utils._polygons_unify(polygons)
        self.assertTrue(shapely.equals(result, expected))

    def test__polygons_unify_impossible_to_unify(self):
        # This is a series of polygons which don't intersect, to see if
        # the code can exit gracefully
        polygons_broken = []
        for i in range(12):
            dist = 1.1 * i
            shape = shapely.Polygon(np.array([[0 + dist, dist],
                                              [0 + dist, 1 + dist],
                                              [1 + dist, 1 + dist],
                                              [1 + dist, dist]]))
            polygons_broken.append(shape)

        dist = 1.1 * 12
        shape_largest = shapely.Polygon(np.array([[0 + dist, dist],
                                                  [0 + dist, 2 + dist],
                                                  [2 + dist, 2 + dist],
                                                  [2 + dist, dist]]))
        polygons_broken.append(shape_largest)
        expected = shape_largest
        result = utils._polygons_unify(polygons_broken)
        self.assertTrue(shapely.equals(result, expected))

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
        X = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
        cdx = np.array([True, True, False, False, True])
        result = utils.IoU_distance_matrix_of_cluster(cdx, X, data)
        expected = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        differance = np.abs(result - expected).flatten()
        # Want it to be within this error
        self.assertTrue(all(differance < 0.001))

    def test_IoU_distance_matrix_cluster_of_one(self):
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
        X = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
        cdx = np.array([True, False, False, False, False])
        result = utils.IoU_distance_matrix_of_cluster(cdx, X, data)
        expected = np.array([[0.]])
        differance = np.abs(result - expected).flatten()
        # Want it to be within this error
        self.assertTrue(all(differance < 0.001))

    def test_IoU_cluster_mean_distance(self):
        distances_matrix = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., 0.85714286],
                            [0.66666667, 0.85714286, 0.]])
        result = utils.IoU_cluster_mean_distance(distances_matrix)
        expected = 0.7301587333333334
        differance = np.abs(result - expected)
        self.assertTrue(differance < 0.00001)

    def test_IoU_cluster_mean_distance_same_user(self):
        distances_matrix = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., np.inf],
                            [0.66666667, np.inf, 0.]])
        result = utils.IoU_cluster_mean_distance(distances_matrix)
        expected = 0.7777777800000001
        differance = np.abs(result - expected)
        self.assertTrue(differance < 0.00001)

    def test_IoU_cluster_mean_distance_cluster_of_one(self):
        distances_matrix = np.array([[0.]])
        result = utils.IoU_cluster_mean_distance(distances_matrix)
        expected = 0.
        differance = np.abs(result - expected)
        self.assertTrue(differance < 0.00001)

    def test_IoU_cluster_mean_distance_non_symmetric(self):
        distances_matrix = np.array([[0., 0.66666667, 0.6666669],
                                    [0.66666667, 0., np.inf],
                                    [0.66666667, np.inf, 0.]])
        with self.assertRaises(Exception) as context:
            utils.IoU_cluster_mean_distance(distances_matrix)

        self.assertTrue('`distances_matrix` must be a symmetric-square array' in str(context.exception))

    def test_IoU_cluster_mean_distance_non_diagonal(self):
        distances_matrix = np.array([[0., 0.66666667, 0.66666667],
                            [0.66666667, 0., np.inf],
                            [0.66666667, np.inf, -10**-5]])
        with self.assertRaises(Exception) as context:
            utils.IoU_cluster_mean_distance(distances_matrix)

        self.assertTrue('`distances_matrix` must have zero diagonal elements, as distance between the object and itself is zero' in str(context.exception))

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

    def test_cluster_average_last_incorrect_data_format(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = [1,
                           datetime.datetime.strptime('2025-01-21 10:46:21', "%Y-%m-%d %H:%M:%S"),
                           datetime.datetime.strptime('2025-01-21 10:46:22', "%Y-%m-%d %H:%M:%S")]
        kwargs = {'created_at': created_at_list}
        with self.assertRaises(Exception) as context:
            utils.cluster_average_last(data, **kwargs)

        self.assertTrue('`created_at` needs to contain either UTC strings, pandas timestamps or datetime objects' in str(context.exception))

    def test_cluster_average_median(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        distance_matrix = np.array([[0., 0.66666667, 0.66666667],
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
        distance_matrix = np.array([[0., np.inf, 0.66666667],
                                    [np.inf, 0., 0.85714286],
                                    [0.66666667, 0.85714286, 0.]])
        kwargs = {'distance_matrix': distance_matrix}
        expected = square3
        result = utils.cluster_average_median(data, **kwargs)
        self.assertEqual(result, expected)

    def test_cluster_average_median_non_symmetric(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        distance_matrix = np.array([[0., np.inf, 0.66666669],
                                    [np.inf, 0., 0.85714286],
                                    [0.66666667, 0.85714286, 0.]])
        kwargs = {'distance_matrix': distance_matrix}
        with self.assertRaises(Exception) as context:
            utils.cluster_average_median(data, **kwargs)

        self.assertTrue('`distances_matrix` must be a symmetric-square array' in str(context.exception))

    def test_cluster_average_median_non_diagonal(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[0.5, 0.0], [0.5, 1.0], [1.5, 1.0], [1.5, 0.0]]))
        square3 = shapely.Polygon(np.array([[0.0, 0.5], [1., 0.5], [1., 1.5], [0.0, 1.5]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        distance_matrix = np.array([[0., np.inf, 0.66666667],
                                    [np.inf, 0., 0.85714286],
                                    [0.66666667, 0.85714286, -10**-5.]])
        kwargs = {'distance_matrix': distance_matrix}
        with self.assertRaises(Exception) as context:
            utils.cluster_average_median(data, **kwargs)

        self.assertTrue('`distances_matrix` must have zero diagonal elements, as distance between the object and itself is zero' in str(context.exception))

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

    def test_cluster_average_intersection_contours(self):
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
        kwargs = {'created_at': created_at_list}
        expected_contour_1 = shapely.Polygon(np.array([[1.5, 0.5],
                                                       [1.5, 0.],
                                                       [1., 0.],
                                                       [0.5, 0.],
                                                       [0., 0.],
                                                       [0., 0.5],
                                                       [0., 1.],
                                                       [0., 1.5],
                                                       [0.5, 1.5],
                                                       [1., 1.5],
                                                       [1.5, 1.5],
                                                       [1.5, 1.],
                                                       [1.5, 0.5]]))
        expected_contour_2 = shapely.Polygon(np.array([[0., 0.5],
                                                       [0., 1.],
                                                       [0.5, 1.],
                                                       [0.5, 1.5],
                                                       [1., 1.5],
                                                       [1., 1.],
                                                       [1.5, 1.],
                                                       [1.5, 0.5],
                                                       [1., 0.5],
                                                       [1., 0.],
                                                       [0.5, 0.],
                                                       [0.5, 0.5],
                                                       [0., 0.5]]))
        expected_contour_3 = shapely.Polygon(np.array([[0.5, 0.5],
                                                       [0.5, 1.],
                                                       [1., 1.],
                                                       [1., 0.5],
                                                       [0.5, 0.5]]))
        expected = [expected_contour_1,
                    expected_contour_2,
                    expected_contour_3,
                    expected_contour_3]
        result = utils.cluster_average_intersection_contours(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    def test_cluster_average_intersection_contours_non_polygon_shapes(self):
        square1 = shapely.Polygon(np.array([[0.2, 0], [0.2, 1], [1.2, 1], [1.2, 0]]))
        square2 = shapely.Polygon(np.array([[1.1, 0], [1.1, 1], [2.1, 1], [2.1, 0]]))
        multipolygon = shapely.MultiPolygon([square1, square2])
        square3 = shapely.Polygon(np.array([[0., 0], [0., 1], [1., 1], [1., 0]]))
        line = shapely.LineString([(0, -1), (0, 1)])
        geometrycollection = shapely.GeometryCollection([square3, line])
        non_simple = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [-1, 0]]))
        non_simplecollection = shapely.MultiPolygon([square1, non_simple])

        data = [{'polygon': multipolygon},
                {'polygon': geometrycollection},
                {'polygon': non_simple},
                {'polygon': non_simplecollection}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC',
                           '2025-01-21 10:36:21 UTC']
        kwargs = {'created_at': created_at_list}
        expected_contour_0 = shapely.Polygon(np.array([[0.2, 1.0],
                                                       [1.0, 1.0],
                                                       [1.1, 1.0],
                                                       [1.2, 1.0],
                                                       [2.1, 1.0],
                                                       [2.1, 0.0],
                                                       [1.2, 0.0],
                                                       [1.1, 0.0],
                                                       [1.0, 0.0],
                                                       [0.2, 0.0],
                                                       [0.0, 0.0],
                                                       [0.0, 0.5],
                                                       [0.0, 1.0],
                                                       [0.2, 1.0]]))
        expected_contour_1 = shapely.Polygon(np.array([[0.2, 0.0],
                                                       [0.2, 0.6],
                                                       [0.0, 0.5],
                                                       [0.0, 1.0],
                                                       [0.2, 1.0],
                                                       [1.0, 1.0],
                                                       [1.2, 1.0],
                                                       [1.2, 0.0],
                                                       [1.0, 0.0],
                                                       [0.2, 0.0]]))
        expected_contour_2 = shapely.Polygon(np.array([[0.2, 1.0],
                                                       [1.0, 1.0],
                                                       [1.0, 0.0],
                                                       [0.2, 0.0],
                                                       [0.2, 0.6],
                                                       [0.0, 0.5],
                                                       [0.0, 1.0],
                                                       [0.2, 1.0]]))
        expected_contour_3 = shapely.Polygon(np.array([[0.2, 0.6],
                                                       [0.2, 1.],
                                                       [1., 1.],
                                                       [0.2, 0.6]]))
        expected = [expected_contour_0,
                    expected_contour_1,
                    expected_contour_2,
                    expected_contour_3,
                    expected_contour_3]
        result = utils.cluster_average_intersection_contours(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    # If there is not one single overall area of intersection, test that the
    # larger one is returned and that it can gracefully exit the algorithm
    def test_cluster_average_intersection_contours_two_final_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[1.5, 0], [1.5, 1], [2.5, 1], [2.5, 0]]))
        square3 = shapely.Polygon(np.array([[0.8, 0], [0.8, 1], [1.8, 1], [1.8, 0]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC']
        kwargs = {'created_at': created_at_list}
        expected_contour_1 = shapely.Polygon(np.array([[0.8, 1.],
                                                       [1., 1.],
                                                       [1.5, 1.],
                                                       [1.8, 1.],
                                                       [2.5, 1.],
                                                       [2.5, 0.],
                                                       [1.8, 0.],
                                                       [1.5, 0.],
                                                       [1., 0.],
                                                       [0.8, 0.],
                                                       [0., 0.],
                                                       [0., 1.],
                                                       [0.8, 1.]]))
        expected_contour_2 = shapely.Polygon(np.array([[1.5, 1.],
                                                       [1.8, 1.],
                                                       [1.8, 0.],
                                                       [1.5, 0.],
                                                       [1.5, 1.]]))
        expected = [expected_contour_1,
                    expected_contour_2]
        result = utils.cluster_average_intersection_contours(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    def test_cluster_average_intersection_contours_rasterisation(self):
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
        kwargs = {'created_at': created_at_list, 'num_grid_points': 50}
        expected_contour_1 = shapely.Polygon(np.array([[0.0, 0.030612244897959183],
                                                       [0.030612244897959183, 0.0],
                                                       [1.4693877551020407, 0.0],
                                                       [1.5, 0.030612244897959183],
                                                       [1.5, 1.4693877551020407],
                                                       [1.4693877551020407, 1.5],
                                                       [0.030612244897959183, 1.5],
                                                       [0.0, 1.4693877551020407],
                                                       [0.0, 0.030612244897959183]]))
        expected_contour_2 = shapely.Polygon(np.array([[0.4897959183673469, 0.030612244897959183],
                                                       [0.5204081632653061, 0.015306122448979591],
                                                       [0.9795918367346939, 0.015306122448979591],
                                                       [1.010204081632653, 0.030612244897959183],
                                                       [1.010204081632653, 0.4897959183673469],
                                                       [1.4693877551020407, 0.4897959183673469],
                                                       [1.4846938775510203, 0.5204081632653061],
                                                       [1.4846938775510203, 0.9795918367346939],
                                                       [1.4693877551020407, 1.010204081632653],
                                                       [1.010204081632653, 1.010204081632653],
                                                       [1.010204081632653, 1.4693877551020407],
                                                       [0.9795918367346939, 1.4846938775510203],
                                                       [0.5204081632653061, 1.4846938775510203],
                                                       [0.4897959183673469, 1.4693877551020407],
                                                       [0.4897959183673469, 1.010204081632653],
                                                       [0.030612244897959183, 1.010204081632653],
                                                       [0.015306122448979591, 0.9795918367346939],
                                                       [0.015306122448979591, 0.5204081632653061],
                                                       [0.030612244897959183, 0.4897959183673469],
                                                       [0.4897959183673469, 0.4897959183673469],
                                                       [0.4897959183673469, 0.030612244897959183]]))
        expected_contour_3 = shapely.Polygon(np.array([[0.4897959183673469, 0.5204081632653061],
                                                       [0.5204081632653061, 0.4897959183673469],
                                                       [0.9795918367346939, 0.4897959183673469],
                                                       [1.010204081632653, 0.5204081632653061],
                                                       [1.010204081632653, 0.9795918367346939],
                                                       [0.9795918367346939, 1.010204081632653],
                                                       [0.5204081632653061, 1.010204081632653],
                                                       [0.4897959183673469, 0.9795918367346939],
                                                       [0.4897959183673469, 0.5204081632653061]]))
        expected_contour_4 = shapely.Polygon(np.array([[0.5051020408163265, 0.5204081632653061],
                                                       [0.5204081632653061, 0.5051020408163265],
                                                       [0.9795918367346939, 0.5051020408163265],
                                                       [0.9948979591836734, 0.5204081632653061],
                                                       [0.9948979591836734, 0.9795918367346939],
                                                       [0.9795918367346939, 0.9948979591836734],
                                                       [0.5204081632653061, 0.9948979591836734],
                                                       [0.5051020408163265, 0.9795918367346939],
                                                       [0.5051020408163265, 0.5204081632653061]]))
        expected = [expected_contour_1,
                    expected_contour_2,
                    expected_contour_3,
                    expected_contour_4]
        result = utils.cluster_average_intersection_contours_rasterisation(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    # If there is not one single overall area of intersection, test that the
    # larger one is returned and that it can gracefully exit the algorithm
    def test_cluster_average_intersection_contours_rasterisation_two_final_intersections(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))
        square2 = shapely.Polygon(np.array([[1.5, 0], [1.5, 1], [2.5, 1], [2.5, 0]]))
        square3 = shapely.Polygon(np.array([[0.8, 0], [0.8, 1], [1.8, 1], [1.8, 0]]))

        data = [{'polygon': square1},
                {'polygon': square2},
                {'polygon': square3}]
        created_at_list = ['2025-01-21 10:46:23 UTC',
                           '2025-01-21 10:46:21 UTC',
                           '2025-01-21 10:46:22 UTC']
        kwargs = {'created_at': created_at_list, 'num_grid_points': 200}
        expected_contour_1 = shapely.Polygon(np.array([[0.0, 0.005025125628140704],
                                                       [2.4874371859296485, 0.0],
                                                       [2.5, 0.005025125628140704],
                                                       [2.5, 0.9949748743718593],
                                                       [0.01256281407035176, 1.0],
                                                       [0.0, 0.9949748743718593],
                                                       [0.0, 0.005025125628140704]]))
        expected_contour_2 = shapely.Polygon(np.array([[1.4949748743718594, 0.005025125628140704],
                                                       [1.8090452261306533, 0.005025125628140704],
                                                       [1.8090452261306533, 0.9949748743718593],
                                                       [1.4949748743718594, 0.9949748743718593],
                                                       [1.4949748743718594, 0.005025125628140704]]))
        expected = [expected_contour_1,
                    expected_contour_2]
        result = utils.cluster_average_intersection_contours_rasterisation(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    # Just use a single polygon, to see if no smoothing works as expected
    def test_cluster_average_intersection_contours_rasterisation_no_smoothing(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1}]
        created_at_list = ['2025-01-21 10:46:23 UTC']
        kwargs = {'created_at': created_at_list,
                  'num_grid_points': 5,
                  'smoothing': 'no_smoothing'}
        expected_contour_1 = shapely.Polygon(np.array([[0.0, 0.25],
                                                       [0.25, 0.0],
                                                       [0.5, 0.0],
                                                       [0.75, 0.0],
                                                       [1.0, 0.25],
                                                       [1.0, 0.5],
                                                       [1.0, 0.75],
                                                       [0.75, 1.0],
                                                       [0.5, 1.0],
                                                       [0.25, 1.0],
                                                       [0.0, 0.75],
                                                       [0.0, 0.5],
                                                       [0.0, 0.25]]))
        expected = [expected_contour_1]
        result = utils.cluster_average_intersection_contours_rasterisation(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))

    # Just use a single polygon, to see if rounded works as expected
    def test_cluster_average_intersection_contours_rasterisation_rounded(self):
        square1 = shapely.Polygon(np.array([[0, 0], [0, 1], [1, 1], [1, 0]]))

        data = [{'polygon': square1}]
        created_at_list = ['2025-01-21 10:46:23 UTC']
        kwargs = {'created_at': created_at_list,
                  'num_grid_points': 5,
                  'smoothing': 'rounded'}
        expected_contour_1 = shapely.Polygon(np.array([[0.04386568069458008, 0.23665213584899902],
                                                       [0.23665213584899902, 0.04386568069458008],
                                                       [0.5, -0.026695728302001953],
                                                       [0.763347864151001, 0.04386568069458008],
                                                       [0.9561343193054199, 0.23665213584899902],
                                                       [1.026695728302002, 0.5],
                                                       [0.9561343193054199, 0.763347864151001],
                                                       [0.763347864151001, 0.9561343193054199],
                                                       [0.5, 1.026695728302002],
                                                       [0.23665213584899902, 0.9561343193054199],
                                                       [0.04386568069458008, 0.763347864151001],
                                                       [-0.026695728302001953, 0.5],
                                                       [0.04386568069458008, 0.23665213584899902]]))
        expected = [expected_contour_1]
        result = utils.cluster_average_intersection_contours_rasterisation(data, **kwargs)
        self.assertTrue(all([shapely.equals(result[i], expected[i]) for i in range(len(expected))]))
