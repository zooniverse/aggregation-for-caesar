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
                    'x': 0
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool1_x': [20]
    },
    'frame1': {
        'T0_tool0_x': [30]
    }
}

TestShapeFullHeightLine = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullHeightLine',
    kwargs={'shape': 'fullHeightLine'}
)

TestShapeFullHeightLineTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullHeightLine with task specified',
    kwargs={
        'shape': 'fullHeightLine',
        'task': 'T0'
    }
)

TestShapeFullHeightLineAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullHeightLine with all tools specified',
    kwargs={
        'shape': 'fullHeightLine',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x']
    },
    'frame1': expected['frame1']
}

TestShapeFullHeightLineOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape fullHeightLine with one tool specified',
    kwargs={
        'shape': 'fullHeightLine',
        'task': 'T0',
        'tools': [0]
    }
)
