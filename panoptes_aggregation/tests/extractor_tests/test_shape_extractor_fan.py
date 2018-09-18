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
                    'radius': 20,
                    'rotation': 15,
                    'spread': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'radius': 30,
                    'rotation': 25,
                    'spread': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'radius': 40,
                    'rotation': 35,
                    'spread': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'radius': 50,
                    'rotation': 45,
                    'spread': 60
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool0_y': [5, 15],
        'T0_tool0_radius': [20, 30],
        'T0_tool0_rotation': [15, 25],
        'T0_tool0_spread': [30, 40],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_radius': [40],
        'T0_tool1_rotation': [35],
        'T0_tool1_spread': [50]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_radius': [50],
        'T0_tool0_rotation': [45],
        'T0_tool0_spread': [60]
    }
}

TestShapeFan = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fan',
    kwargs={'shape': 'fan'}
)

TestShapeFanTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fan with task specified',
    kwargs={
        'shape': 'fan',
        'task': 'T0'
    }
)

TestShapeFanAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fan with all tools specified',
    kwargs={
        'shape': 'fan',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_radius': expected['frame0']['T0_tool0_radius'],
        'T0_tool0_rotation': expected['frame0']['T0_tool0_rotation'],
        'T0_tool0_spread': expected['frame0']['T0_tool0_spread']
    },
    'frame1': expected['frame1']
}

TestShapeFanOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape fan with one tool specified',
    kwargs={
        'shape': 'fan',
        'task': 'T0',
        'tools': [0]
    }
)
