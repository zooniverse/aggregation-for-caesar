import unittest
import numpy
import shapely.geometry
import shapely.affinity
import panoptes_aggregation.reducers.shape_metric_IoU as IoU


class TestIoUMetric(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_panoptes_to_geometry_rect(self):
        '''Test panoptes_to_geometry with rectangle'''
        expected = shapely.geometry.box(3, 5, 8, 8)
        result = IoU.panoptes_to_geometry([3, 5, 5, 3], 'rectangle')
        self.assertEqual(result, expected)

    def test_panoptes_to_geometry_rot_rect(self):
        '''Test panoptes_to_geometry with rotating rectangle'''
        expected = shapely.geometry.box(3, 5, 8, 8)
        expected = shapely.affinity.rotate(expected, 45)
        result = IoU.panoptes_to_geometry([3, 5, 5, 3, 45], 'rotateRectangle')
        self.assertEqual(result, expected)

    def test_panoptes_to_geometry_circle(self):
        '''Test panoptes_to_geometry with circle'''
        expected = shapely.geometry.Point(10, 12).buffer(5)
        result = IoU.panoptes_to_geometry([10, 12, 5], 'circle')
        self.assertEqual(result, expected)

    def test_panoptes_to_geometry_ellipse(self):
        '''Test panoptes_to_geometry with ellipse'''
        expected = shapely.geometry.Point(10, 12).buffer(1)
        expected = shapely.affinity.scale(expected, 3, 5)
        expected = shapely.affinity.rotate(expected, -45)
        result = IoU.panoptes_to_geometry([10, 12, 3, 5, 45], 'ellipse')
        self.assertEqual(result, expected)

    def test_panoptes_to_geometry_triangle(self):
        '''Test panoptes_to_geometry with triangle'''
        expected = shapely.geometry.Polygon([
            [0, -3],
            [3 * numpy.sqrt(3) / 2, 3 / 2],
            [-3 * numpy.sqrt(3) / 2, 3 / 2]
        ])
        expected = shapely.affinity.rotate(expected, -30, origin=(0, 0))
        expected = shapely.affinity.translate(expected, xoff=5, yoff=10)
        result = IoU.panoptes_to_geometry([5, 10, 3, 30], 'triangle')
        self.assertEqual(result, expected)

    def test_panoptes_to_geometry_other(self):
        '''Test panoptes_to_geometry with unsupported shape'''
        with self.assertRaises(ValueError):
            IoU.panoptes_to_geometry([1], 'not_a_supported_shape')

    def test_IoU_metric(self):
        '''Test the IoU metric'''
        expected = [0, 0.5, 1]
        shape = 'rectangle'
        shape1 = [0, 0, 2, 2]
        shape2 = [
            [0, 0, 2, 2],
            [0, 2 / 3, 2, 2],
            [0, 2, 2, 2]
        ]
        for e, s2 in zip(expected, shape2):
            with self.subTest(s2=s2):
                result = IoU.IoU_metric(shape1, s2, shape)
                numpy.testing.assert_almost_equal(result, e, 5)

    def test_IoU_metric_no_area(self):
        '''Test the IoU metirc no area shapes'''
        expected = numpy.inf
        # circle with radius zero
        result = IoU.IoU_metric([0, 0, 0], [1, 1, 0], 'circle')
        self.assertEqual(result, expected)

    def test_average_bounds_rect(self):
        '''Test finding the average bounds for rectangles'''
        params_list = [
            [0, 0, 2, 2],
            [0, 2, 2, 2],
            [0, 2, 2, 3]
        ]
        expected = [
            (0, 2),
            (0, 5),
            (1, 2),
            (1, 5)
        ]
        result = IoU.average_bounds(params_list, 'rectangle')
        self.assertEqual(result, expected)

    def test_average_bounds_rot_rect(self):
        '''Test finding the average bounds for rotating rectangles'''
        params_list = [
            [0, 0, 2, 2, 180],
            [0, 2, 2, 2, 0],
            [0, 2, 2, 3, 180]
        ]
        expected = [
            (0, 2),
            (0, 5),
            (1, 2),
            (1, 5),
            (0, 180)
        ]
        result = IoU.average_bounds(params_list, 'rotateRectangle')
        self.assertEqual(result, expected)

    def test_average_bounds_ellipse(self):
        '''Test finding the average bounds for the ellipse'''
        params_list = [
            [0, 0, 2, 2, 180],
            [0, 2, 2, 2, 180],
            [0, 2, 2, 3, 180]
        ]
        expected = [
            (-2, 2),
            (-2, 5),
            (1, 4),
            (1, 7),
            (0, 180)
        ]
        result = IoU.average_bounds(params_list, 'ellipse')
        self.assertEqual(result, expected)

    def test_average_bounds_circle(self):
        '''Test finding the average bounds for circles'''
        params_list = [
            [0, 0, 2],
            [0, 2, 2],
            [0, 1, 2]
        ]
        expected = [
            (-2, 2),
            (-2, 4),
            (1, 6),
        ]
        result = IoU.average_bounds(params_list, 'circle')
        self.assertEqual(result, expected)

    def test_average_bounds_triangle(self):
        params_list = [
            [0, 0, 2, 0],
            [0, 2, 2, 60],
            [0, 1, 2, 120]
        ]
        expected = [
            (-numpy.sqrt(3), numpy.sqrt(3)),
            (-2.0, 4.0),
            (1, 6.0),
            (0, 120)
        ]
        result = IoU.average_bounds(params_list, 'triangle')
        numpy.testing.assert_allclose(result, expected)

    def test_scale_shape(self):
        '''Test scale_shape for various shapes'''
        shapes = [
            'rectangle',
            'rotateRectangle',
            'circle',
            'ellipse',
            'triangle'
        ]
        gamma = 2
        params = [
            [10, 10, 2, 4],
            [10, 10, 2, 4, 45],
            [5, 5, 2],
            [10, 10, 3, 2, 30],
            [5, 5, 2, 30]
        ]
        expectations = [
            [9, 8, 4, 8],
            [9, 8, 4, 8, 45],
            [5, 5, 4],
            [10, 10, 6, 4, 30],
            [5, 5, 4, 30]
        ]
        for shape, param, expected in zip(shapes, params, expectations):
            with self.subTest(shape=shape, params=params):
                result = IoU.scale_shape(param, shape, gamma)
                self.assertEqual(result, expected)

    def test_scale_shape_other(self):
        '''Test scale_shape with unsupported shape'''
        with self.assertRaises(ValueError):
            IoU.scale_shape([1], 2, 'not_a_supported_shape')

    def test_average_shapes(self):
        '''Test taking the average of four rectangles'''
        shape = 'rectangle'
        params = [
            [1, 0, 2, 2],
            [0, 1, 2, 2],
            [2, 1, 2, 2],
            [1, 2, 2, 2]
        ]
        expected_avg = [1, 1, 2, 2]
        expected_sigma = 4.0 / numpy.sqrt(27)
        result = IoU.average_shape_IoU(params, shape)
        result_avg, result_sigma = result
        numpy.testing.assert_allclose(result_avg, expected_avg, 3)
        numpy.testing.assert_almost_equal(result_sigma, expected_sigma, 3)

    def test_sigma_shape(self):
        '''Test making 1-sigma scaled rectangle'''
        shape = 'rectangle'
        params = [1, 1, 2, 2]
        sigma = 0.5
        expected_avg_minus_sigma = IoU.scale_shape(params, shape, 1 / numpy.sqrt(2))
        expected_avg_plus_sigma = IoU.scale_shape(params, shape, numpy.sqrt(2))
        result_plus_sigma, result_minus_sigma = IoU.sigma_shape(params, shape, sigma)
        numpy.testing.assert_allclose(result_minus_sigma, expected_avg_minus_sigma, 3)
        numpy.testing.assert_allclose(result_plus_sigma, expected_avg_plus_sigma, 3)
