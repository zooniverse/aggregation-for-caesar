from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [
        {
            'task': 'T2',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 0,
                    'y': 0,
                    'width': 5,
                    'height': 10,
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'width': 10,
                    'height': 5,
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 100,
                    'y': 90,
                    'width': 24,
                    'height': 24,
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 110,
                    'y': 91,
                    'width': 27,
                    'height': 50,
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T2_tool0_x': [0, 20],
        'T2_tool0_y': [0, 25],
        'T2_tool0_width': [5, 10],
        'T2_tool0_height': [10, 5],
        'T2_tool1_x': [100],
        'T2_tool1_y': [90],
        'T2_tool1_width': [24],
        'T2_tool1_height': [24],
    },
    'frame1': {
        'T2_tool0_x': [110],
        'T2_tool0_y': [91],
        'T2_tool0_width': [27],
        'T2_tool0_height': [50],
    }
}

TestRectangle = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test rectangle'
)

TestRectangleTask = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test rectangle with task specified',
    kwargs={'task': 'T2'}
)

TestRectangleAllTools = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test rectangle with all tools specified',
    kwargs={
        'task': 'T2',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T2_tool0_x': expected['frame0']['T2_tool0_x'],
        'T2_tool0_y': expected['frame0']['T2_tool0_y'],
        'T2_tool0_width': expected['frame0']['T2_tool0_width'],
        'T2_tool0_height': expected['frame0']['T2_tool0_height']
    },
    'frame1': expected['frame1']
}

TestRectangleOneTool = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected_0,
    'Test rectangle one tool specified',
    kwargs={
        'task': 'T2',
        'tools': [0]
    }
)
