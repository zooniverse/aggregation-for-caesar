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
                    'x': 0,
                    'y': 5
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool0_y': [5, 15],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35]
    }
}

TestShapePoint = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape point',
    kwargs={'shape': 'point'}
)

TestShapePointTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape point with task specified',
    kwargs={
        'shape': 'point',
        'task': 'T0'
    }
)

TestShapePointAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape point with all tools specified',
    kwargs={
        'shape': 'point',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y']
    },
    'frame1': expected['frame1']
}

TestShapePointOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape point with one tool specified',
    kwargs={
        'shape': 'point',
        'task': 'T0',
        'tools': [0]
    }
)
