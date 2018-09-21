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
                    'width': 20,
                    'height': 15,
                    'angle': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'width': 30,
                    'height': 25,
                    'angle': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'width': 40,
                    'height': 35,
                    'angle': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'width': 50,
                    'height': 45,
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
        'T0_tool0_width': [20, 30],
        'T0_tool0_height': [15, 25],
        'T0_tool0_angle': [30, 40],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_width': [40],
        'T0_tool1_height': [35],
        'T0_tool1_angle': [50]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_width': [50],
        'T0_tool0_height': [45],
        'T0_tool0_angle': [60]
    }
}

TestShapeRotateRectangle = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rotateRectangle',
    kwargs={'shape': 'rotateRectangle'}
)

TestShapeRotateRectangleTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rotateRectangle with task specified',
    kwargs={
        'shape': 'rotateRectangle',
        'task': 'T0'
    }
)

TestShapeRotateRectangleAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rotateRectangle with all tools specified',
    kwargs={
        'shape': 'rotateRectangle',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_width': expected['frame0']['T0_tool0_width'],
        'T0_tool0_height': expected['frame0']['T0_tool0_height'],
        'T0_tool0_angle': expected['frame0']['T0_tool0_angle']
    },
    'frame1': expected['frame1']
}

TestShapeRotateRectangleOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape rotateRectangle with one tool specified',
    kwargs={
        'shape': 'rotateRectangle',
        'task': 'T0',
        'tools': [0]
    }
)
