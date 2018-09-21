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
                    'y': 0
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'y': 10
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'y': 20
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'y': 30
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_y': [0, 10],
        'T0_tool1_y': [20]
    },
    'frame1': {
        'T0_tool0_y': [30]
    }
}

TestShapeFullWidthLine = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullWidthLine',
    kwargs={'shape': 'fullWidthLine'}
)

TestShapeFullWidthLineTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullWidthLine with task specified',
    kwargs={
        'shape': 'fullWidthLine',
        'task': 'T0'
    }
)

TestShapeFullWidthLineAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape fullWidthLine with all tools specified',
    kwargs={
        'shape': 'fullWidthLine',
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_y': expected['frame0']['T0_tool0_y']
    },
    'frame1': expected['frame1']
}

TestShapeFullWidthLineOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape fullWidthLine with one tool specified',
    kwargs={
        'shape': 'fullWidthLine',
        'task': 'T0',
        'tools': [0]
    }
)
