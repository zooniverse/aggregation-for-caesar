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
                    'x1': 0,
                    'y1': 5,
                    'x2': 20,
                    'y2': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x1': 10,
                    'y1': 15,
                    'x2': 30,
                    'y2': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x1': 20,
                    'y1': 25,
                    'x2': 40,
                    'y2': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x1': 30,
                    'y1': 35,
                    'x2': 50,
                    'y2': 60
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x1': [0, 10],
        'T0_tool0_y1': [5, 15],
        'T0_tool0_x2': [20, 30],
        'T0_tool0_y2': [30, 40],
        'T0_tool1_x1': [20],
        'T0_tool1_y1': [25],
        'T0_tool1_x2': [40],
        'T0_tool1_y2': [50]
    },
    'frame1': {
        'T0_tool0_x1': [30],
        'T0_tool0_y1': [35],
        'T0_tool0_x2': [50],
        'T0_tool0_y2': [60]
    }
}

TestShapeLine = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line',
    kwargs={'shape': 'line'}
)

TestShapeLineTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line with task specified',
    kwargs={
        'shape': 'line',
        'task': 'T0'
    }
)

TestShapeLineAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line with all tools specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x1': expected['frame0']['T0_tool0_x1'],
        'T0_tool0_y1': expected['frame0']['T0_tool0_y1'],
        'T0_tool0_x2': expected['frame0']['T0_tool0_x2'],
        'T0_tool0_y2': expected['frame0']['T0_tool0_y2']
    },
    'frame1': expected['frame1']
}

TestShapeLineOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape line with one tool specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0]
    }
)
