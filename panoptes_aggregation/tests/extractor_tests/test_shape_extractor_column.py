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
    kwargs={'shape': 'column'},
    test_name='TestShapeColumn'
)

TestShapeColumnTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column with task specified',
    kwargs={
        'shape': 'column',
        'task': 'T0'
    },
    test_name='TestShapeColumnTask'
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
    },
    test_name='TestShapeColumnAllTools'
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
    },
    test_name='TestShapeColumnOneTool'
)

classification_blank = {
    'annotations': [
        {
            'task': 'T0',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'x': None,
                    'width': None
                }
            ]
        }
    ]
}

expected_blank = {}

TestShapeColumnBlank = ExtractorTest(
    extractors.shape_extractor,
    classification_blank,
    expected_blank,
    'Test shape column with blank classification',
    kwargs={
        'shape': 'column',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeColumnBlank'
)

classification_v2 = {
    'annotations': [
        {
            'task': 'T0',
            'taskType': 'dataVisAnnotation',
            'value': [
                {
                    'toolIndex': 0,
                    'toolType': 'graph2dRangeX',
                    'x': 0,
                    'width': 5
                },
                {
                    'toolIndex': 0,
                    'toolType': 'graph2dRangeX',
                    'x': 10,
                    'width': 15
                },
                {
                    'toolIndex': 1,
                    'toolType': 'graph2dRangeX',
                    'x': 20,
                    'width': 25
                }
            ]
        }
    ],
    'metadata': {
        'classifier_version': '2.0'
    }
}

expected_v2 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [0, 10],
        'T0_toolIndex0_width': [5, 15],
        'T0_toolIndex1_x': [20],
        'T0_toolIndex1_width': [25],
    }
}

TestShapeGraph2dRangeX_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape graph2dRangeX',
    kwargs={'shape': 'graph2dRangeX'},
    test_name='TestShapeGraph2dRangeX_v2'
)

TestShapeColumn_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape column V2',
    kwargs={'shape': 'column'},
    test_name='TestShapeColumn_v2'
)

TestShapeGraph2dRangeXTask_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape graph2dRangeX with task specified',
    kwargs={
        'shape': 'graph2dRangeX',
        'task': 'T0'
    },
    test_name='TestShapeGraph2dRangeXTask_v2'
)

TestShapeColumnTask_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape  column V2 with task specified',
    kwargs={
        'shape': 'column',
        'task': 'T0'
    },
    test_name='TestShapeColumnTask_v2'
)

TestShapeGraph2dRangeXAllTools_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape graph2dRangeX with all tools specified',
    kwargs={
        'shape': 'graph2dRangeX',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeGraph2dRangeXAllTools_v2'
)

TestShapeColumnAllTools_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape  column V2 with all tools specified',
    kwargs={
        'shape': 'column',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeColumnAllTools_v2'
)

expected_v2_0 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [0, 10],
        'T0_toolIndex0_width': [5, 15],
    }
}

TestShapeGraph2dRangeXOneTool_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2_0,
    'Test shape graph2dRangeX with one tool specified',
    kwargs={
        'shape': 'graph2dRangeX',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeGraph2dRangeXOneTool_v2'
)

TestShapeColumnOneTool_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2_0,
    'Test shape  column V2 with one tool specified',
    kwargs={
        'shape': 'column',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeColumnOneTool_v2'
)
