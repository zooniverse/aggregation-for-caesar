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
                    'rx': 20,
                    'ry': 15,
                    'angle': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'rx': 30,
                    'ry': 25,
                    'angle': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'rx': 40,
                    'ry': 35,
                    'angle': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'rx': 50,
                    'ry': 45,
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
        'T0_tool0_rx': [20, 30],
        'T0_tool0_ry': [15, 25],
        'T0_tool0_angle': [30, 40],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_rx': [40],
        'T0_tool1_ry': [35],
        'T0_tool1_angle': [50]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_rx': [50],
        'T0_tool0_ry': [45],
        'T0_tool0_angle': [60]
    }
}

TestShapeEllipse = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape ellipse',
    kwargs={'shape': 'ellipse'}
)

TestShapeEllipseTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape ellipse with task specified',
    kwargs={
        'shape': 'ellipse',
        'task': 'T0'
    }
)

TestShapeEllipseAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape ellipse with all tools specified',
    kwargs={
        'shape': 'ellipse',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_rx': expected['frame0']['T0_tool0_rx'],
        'T0_tool0_ry': expected['frame0']['T0_tool0_ry'],
        'T0_tool0_angle': expected['frame0']['T0_tool0_angle']
    },
    'frame1': expected['frame1']
}

TestShapeEllipseOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape ellipse with one tool specified',
    kwargs={
        'shape': 'ellipse',
        'task': 'T0',
        'tools': [0]
    }
)
