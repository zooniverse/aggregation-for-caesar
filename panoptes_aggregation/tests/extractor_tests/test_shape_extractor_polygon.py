from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [
        {
            'task': 'T0',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [
                        {'x': 0, 'y': 0},
                        {'x': 10, 'y': 0},
                        {'x': 10, 'y': 10}
                    ],
                    'closed': True
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'points': [
                        {'x': 10, 'y': 0},
                        {'x': 20, 'y': 0},
                        {'x': 20, 'y': 10}
                    ],
                    'closed': True
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'points': [
                        {'x': 0, 'y': 10},
                        {'x': 10, 'y': 10},
                        {'x': 10, 'y': 20}
                    ],
                    'closed': True
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'points': [
                        {'x': 10, 'y': 10},
                        {'x': 20, 'y': 10},
                        {'x': 20, 'y': 20}
                    ],
                    'closed': True
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_points_x': [
            [0, 10, 10],
            [10, 20, 20]
        ],
        'T0_tool0_points_y': [
            [0, 0, 10],
            [0, 0, 10]
        ],
        'T0_tool0_closed': [
            True,
            True
        ],
        'T0_tool1_points_x': [
            [0, 10, 10]
        ],
        'T0_tool1_points_y': [
            [10, 10, 20]
        ],
        'T0_tool1_closed': [
            True
        ]
    },
    'frame1': {
        'T0_tool0_points_x': [
            [10, 20, 20]
        ],
        'T0_tool0_points_y': [
            [10, 10, 20],
        ],
        'T0_tool0_closed': [
            True
        ]
    }
}

TestPolygon = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape polygon',
    kwargs={'shape': 'polygon'}
)

TestPolygonTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape polygon with task specified',
    kwargs={
        'shape': 'polygon',
        'task': 'T0'
    }
)

TestPolygonAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape polygon with all tools specified',
    kwargs={
        'shape': 'polygon',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_points_x': expected['frame0']['T0_tool0_points_x'],
        'T0_tool0_points_y': expected['frame0']['T0_tool0_points_y'],
        'T0_tool0_closed': expected['frame0']['T0_tool0_closed']
    },
    'frame1': expected['frame1']
}

TestPolygonOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape polygon with one tool specified',
    kwargs={
        'shape': 'polygon',
        'task': 'T0',
        'tools': [0]
    }
)
