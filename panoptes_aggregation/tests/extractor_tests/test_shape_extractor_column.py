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
                    'width': 5
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'width': 15
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'width': 25
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'width': 35
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool0_width': [5, 15],
        'T0_tool1_x': [20],
        'T0_tool1_width': [25],
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_width': [35],
    }
}

TestShapeColumn = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column',
    kwargs={'shape': 'column'}
)

TestShapeColumnTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column with task specified',
    kwargs={
        'shape': 'column',
        'task': 'T0'
    }
)

TestShapeColumnAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column with all tools specified',
    kwargs={
        'shape': 'column',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_width': expected['frame0']['T0_tool0_width'],
    },
    'frame1': expected['frame1']
}

TestShapeColumnOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape column with one tool specified',
    kwargs={
        'shape': 'column',
        'task': 'T0',
        'tools': [0]
    }
)
