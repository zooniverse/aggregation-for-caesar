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
                    'y': 5,
                    'r': 20,
                    'angle': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'r': 30,
                    'angle': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'r': 40,
                    'angle': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'r': 50,
                    'angle': 60
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool0_y': [5, 15],
        'T0_tool0_r': [20, 30],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_r': [40]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_r': [50]
    }
}

TestShapeCircle = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle',
    kwargs={'shape': 'circle'}
)

TestShapeCircleTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle with task specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0'
    }
)

TestShapeCircleAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle with all tools specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_r': expected['frame0']['T0_tool0_r']
    },
    'frame1': expected['frame1']
}

TestShapeCircleOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape circle with one tool specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0]
    }
)
