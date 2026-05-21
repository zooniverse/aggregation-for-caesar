import unittest
from panoptes_aggregation.reducers.shape_normalization import SHAPE_NORMALIZATION, SHAPE_VERSION_CONVERT

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
expected_ellipse_convert = [
    (0, 0, 30, 20, -20),
    (0, 0, 30, 20, 160),
    (0, 0, 20, 30, -110)
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

test_rot_rectangle_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, -160),
    (5, -5, 20, 30, 110)
]
expected_rot_rectangle_norm = [
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20),
    (0, 0, 30, 20, 20)
]
expected_rot_rectangle_convert = [
    (15, 10, 30, 20, 20),
    (15, 10, 30, 20, -160),
    (15, 10, 20, 30, 110)
]
expected_rot_rectangle_convert_norm = [
    (15, 10, 30, 20, 20),
    (15, 10, 30, 20, 20),
    (15, 10, 30, 20, 20)
]


test_rectangle = [
    (0, 0, 30, 20),
    (0, 0, 30, 20),
    (5, -5, 20, 30)
]
expected_rectangle_convert = [
    (15, 10, 30, 20),
    (15, 10, 30, 20),
    (15, 10, 20, 30)
]

test_circle = [
    (0, 0, 1),
    (1, 1, 1),
    (2, 1, 2)
]

test_line = [
    (0, 0, 1, 5),
    (1, 1, 1, 3),
    (2, 1, 2, 1)
]

test_point = [
    (0, 0),
    (1, 1),
    (2, 1)
]



class ShapeMetrics(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def normalizationCheck(self, test, expected, shape, **kwargs):
        normalization_function = SHAPE_NORMALIZATION[shape]
        for i in range(len(test)):
            with self.subTest(i=i):
                result = normalization_function(test[i], **kwargs)
                self.assertEqual(result, expected[i])

    def convertCheck(self, test, expected, shape):
        normalization_function = SHAPE_VERSION_CONVERT[shape]
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

    def testEllipseConvert(self):
        '''Test ellipse v1.0 to v2.0 conversion'''
        self.convertCheck(
            test_ellipse_norm,
            expected_ellipse_convert,
            'ellipse'
        )

    def testLineNormalize(self):
        '''Test line normalization'''
        self.normalizationCheck(
            test_line_norm,
            expected_line_norm,
            'line'
        )

    def testLineConvert(self):
        '''Test line normalization'''
        self.convertCheck(
            test_line_norm,
            test_line_norm,
            'line'
        )

    def testTriangleNormalize(self):
        '''Test triangle normalization'''
        self.normalizationCheck(
            test_triangle_norm,
            expected_triangle_norm,
            'triangle'
        )

    def testRotRectangleNormalizeV1(self):
        '''Test rotating rectangle normalization V1.0'''
        self.normalizationCheck(
            test_rot_rectangle_norm,
            expected_rot_rectangle_norm,
            'rotateRectangle'
        )

    def testRotRectangleNormalizeV2(self):
        '''Test rotating rectangle normalization V2.0'''
        self.normalizationCheck(
            expected_rot_rectangle_convert,
            expected_rot_rectangle_convert_norm,
            'rotateRectangle',
            classifier_version='2.0'
        )

    def testRotRectangleConvert(self):
        self.convertCheck(
            test_rot_rectangle_norm,
            expected_rot_rectangle_convert,
            'rotateRectangle'
        )

    def testRectangleConvert(self):
        self.convertCheck(
            test_rectangle,
            expected_rectangle_convert,
            'rectangle'
        )
    
    def testCircleConvert(self):
        self.convertCheck(
            test_circle,
            test_circle,
            'circle'
        )

    def testLineConvert(self):
        self.convertCheck(
            test_line,
            test_line,
            'line'
        )

    def testPointConvert(self):
        self.convertCheck(
            test_point,
            test_point,
            'point'
        )
