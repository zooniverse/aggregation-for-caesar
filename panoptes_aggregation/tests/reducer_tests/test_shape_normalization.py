import unittest
from panoptes_aggregation.reducers.shape_normalization import SHAPE_NORMALIZATION

test_ellipse_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, -160),
    (0, 0, 20, 30, 110)
]
expected_ellipse_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20)
]

test_line_norm = [
    (0, 5, 50, 55),
    (50, 55, 0, 5),
    (0, 5, 0, 55),
    (0, 55, 0, 5)
]
expected_line_norm = [
    (0, 5, 50, 55),
    (0, 5, 50, 55),
    (0, 5, 0, 55),
    (0, 5, 0, 55)
]

test_triangle_norm = [
    (0, 0, 10, 0),
    (0, 0, 10, 120),
    (0, 0, 10, -120),
    (0, 0, 10, 180)
]
expected_triangle_norm = [
    (0, 0, 10, 0),
    (0, 0, 10, 0),
    (0, 0, 10, 0),
    (0, 0, 10, 60)
]

test_rectangle_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, -160),
    (5, -5, 20, 30, 110)
]
expected_rectangle_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20)
]


class ShapeMetrics(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def normalizationCheck(self, test, expected, shape):
        normalization_function = SHAPE_NORMALIZATION[shape]
        for i in range(len(test)):
            with self.subTest(i=i):
                result = normalization_function(test[i])
                self.assertEqual(result, expected[i])

    def testEllipseNormalize(self):
        '''Test ellipse normalization'''
        self.normalizationCheck(
            test_ellipse_norm,
            expected_ellipse_norm,
            'ellipse'
        )

    def testLineNormalize(self):
        '''Test line normalization'''
        self.normalizationCheck(
            test_line_norm,
            expected_line_norm,
            'line'
        )

    def testTriangleNormalize(self):
        '''Test triangle normalization'''
        self.normalizationCheck(
            test_triangle_norm,
            expected_triangle_norm,
            'triangle'
        )

    def testRectangleNormalize(self):
        '''Test triangle normalization'''
        self.normalizationCheck(
            test_rectangle_norm,
            expected_rectangle_norm,
            'rotateRectangle'
        )
