from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest
import unittest

classification = {
    'annotations': [
        {
            'task': 'T0',
            'task_label': 'Draw some lines',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [
                        {'x': -0.011871167727739784, 'y': 0.361724434930079},
                        {'x': -0.28870602933343953, 'y': 0.21452872800162825},
                        {'x': -0.38037475471301413, 'y': -0.08530616243925668},
                        {'x': -0.2331790477845634, 'y': -0.3621410240449564},
                        {'x': 0.06665584265632145, 'y': -0.453809749424531},
                        {'x': 0.3434907042620213, 'y': -0.30661404249608026},
                        {'x': 0.4351594296415958, 'y': -0.006779152055195435},
                        {'x': 0.2879637227131452, 'y': 0.2700557095505044},
                        {'x': -0.0118711677277397, 'y': 0.36172443493007894}
                    ],
                    'details': [],
                    'tool_label': 'Tool name'
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [
                        {'x': 4.630602319839481, 'y': 3.855330076852154},
                        {'x': 5.081828653996981, 'y': 3.615408779166577},
                        {'x': 5.449443973123015, 'y': 3.9704107662937083},
                        {'x': 5.225416400970543, 'y': 4.429735358097605},
                        {'x': 4.719344427837162, 'y': 4.358611580573953},
                        {'x': 4.630602319839481, 'y': 3.8553300768521543}
                    ],
                    'details': [],
                    'tool_label': 'Tool name'
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [
                        {'x': -1.726260190173002, 'y': 2.2716019279274726},
                        {'x': -2.14338918482516, 'y': 2.2643209142423775},
                        {'x': -2.3456481393346444, 'y': 1.8994361013759973},
                        {'x': -2.1307780991919705, 'y': 1.5418323021947127},
                        {'x': -1.7136491045398121, 'y': 1.5491133158798083},
                        {'x': -1.5113901500303277, 'y': 1.9139981287461882},
                        {'x': -1.726260190173002, 'y': 2.2716019279274726}
                    ],
                    'details': [],
                    'tool_label': 'Tool name'
                },
                {
                    'toolIndex': 1,
                    'frame': 0,
                    'pathX': [0., 1, 1., 0., 0.],
                    'pathY': [0., 0., 1., 1., 0.],
                    'details': [],
                    'tool_label': 'Tool name'
                }
            ]
        },
        {
            'task': 'T0',
            'task_label': 'Draw some lines',
            'value': []
        },
        {
            'task': 'T0',
            'task_label': 'Draw some lines',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [],
                    'details': [],
                    'tool_label': 'Tool name'
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_pathX': [
            [
                -0.011871167727739784,
                -0.28870602933343953,
                -0.38037475471301413,
                -0.2331790477845634,
                0.06665584265632145,
                0.3434907042620213,
                0.4351594296415958,
                0.2879637227131452,
                -0.0118711677277397
            ], [
                4.630602319839481,
                5.081828653996981,
                5.449443973123015,
                5.225416400970543,
                4.719344427837162,
                4.630602319839481
            ], [
                -1.726260190173002,
                -2.14338918482516,
                -2.3456481393346444,
                -2.1307780991919705,
                -1.7136491045398121,
                -1.5113901500303277,
                -1.726260190173002
            ]
        ],
        'T0_tool0_pathY': [
            [
                0.361724434930079,
                0.21452872800162825,
                -0.08530616243925668,
                -0.3621410240449564,
                -0.453809749424531,
                -0.30661404249608026,
                -0.006779152055195435,
                0.2700557095505044,
                0.36172443493007894
            ], [
                3.855330076852154,
                3.615408779166577,
                3.9704107662937083,
                4.429735358097605,
                4.358611580573953,
                3.8553300768521543
            ], [
                2.2716019279274726,
                2.2643209142423775,
                1.8994361013759973,
                1.5418323021947127,
                1.5491133158798083,
                1.9139981287461882,
                2.2716019279274726
            ]
        ],
        'T0_toolIndex1_pathX': [
            [
                0.0,
                1,
                1.0,
                0.0,
                0.0
            ]
        ],
        'T0_toolIndex1_pathY': [
            [
                0.0,
                0.0,
                1.0,
                1.0,
                0.0
            ]
        ],
        'gold_standard': False
    }
}


TestPolygon = ExtractorTest(
    extractors.polygon_extractor,
    classification,
    expected,
    'Test polygon',
    test_name='TestPolygon'
)

TestPolygonTask = ExtractorTest(
    extractors.polygon_extractor,
    classification,
    expected,
    'Test polygon with task specified',
    kwargs={
        'task': 'T0'
    },
    test_name='TestPolygonTask'
)

# Now let's test if an error is thrown for incorrect data inputs
classification_incorrect_tool = {
    'annotations': [
        {
            'task': 'T0',
            'task_label': 'Draw some lines',
            'value': [
                {
                    'index': 0,
                    'frame': 0,
                    'pathX': [0., 1, 1., 0., 0.],
                    'pathY': [0., 0., 1., 1., 0.],
                    'details': [],
                    'tool_label': 'Tool name'
                }
            ]
        }
    ]
}


# Test error is correctly thrown
class TestException(unittest.TestCase):
    def testexception_tool(self):
        with self.assertRaises(Exception) as context:
            extractors.polygon_extractor._original(classification_incorrect_tool)

        self.assertTrue('Neither `tool` or `toolIndex` are in the annotation' in str(context.exception))

    def testexception_format(self):
        classification_incorrect_x_y_format = {
            'annotations': [
                {
                    'task': 'T0',
                    'task_label': 'Draw some lines',
                    'value': [
                        {
                            'tool': 0,
                            'frame': 0,
                            'X': [0., 1, 1., 0., 0.],
                            'Y': [0., 0., 1., 1., 0.],
                            'details': [],
                            'tool_label': 'Tool name'
                        }
                    ]
                }
            ]
        }
        with self.assertRaises(Exception) as context:
            extractors.polygon_extractor._original(classification_incorrect_x_y_format)

        self.assertTrue('Unknown data format for polygon data' in str(context.exception))
