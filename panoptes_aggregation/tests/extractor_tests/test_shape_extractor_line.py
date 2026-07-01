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
                    'x1': 0,
                    'y1': 5,
                    'x2': 20,
                    'y2': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x1': 10,
                    'y1': 15,
                    'x2': 30,
                    'y2': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x1': 20,
                    'y1': 25,
                    'x2': 40,
                    'y2': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x1': 30,
                    'y1': 35,
                    'x2': 50,
                    'y2': 60
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x1': [0, 10],
        'T0_tool0_y1': [5, 15],
        'T0_tool0_x2': [20, 30],
        'T0_tool0_y2': [30, 40],
        'T0_tool1_x1': [20],
        'T0_tool1_y1': [25],
        'T0_tool1_x2': [40],
        'T0_tool1_y2': [50]
    },
    'frame1': {
        'T0_tool0_x1': [30],
        'T0_tool0_y1': [35],
        'T0_tool0_x2': [50],
        'T0_tool0_y2': [60]
    }
}

TestShapeLine = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line',
    kwargs={'shape': 'line'},
    test_name='TestShapeLine'
)

TestShapeLineTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line with task specified',
    kwargs={
        'shape': 'line',
        'task': 'T0'
    },
    test_name='TestShapeLineTask'
)

TestShapeLineAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape line with all tools specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeLineAllTools'
)

expected_0 = {
    'frame0': {
        'T0_tool0_x1': expected['frame0']['T0_tool0_x1'],
        'T0_tool0_y1': expected['frame0']['T0_tool0_y1'],
        'T0_tool0_x2': expected['frame0']['T0_tool0_x2'],
        'T0_tool0_y2': expected['frame0']['T0_tool0_y2']
    },
    'frame1': expected['frame1']
}

TestShapeLineOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape line with one tool specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeLineOneTool'
)

classification_v2 = {
    'annotations': [
        {
            'task': 'T0',
            'taskType': 'drawing',
            'value': [
                {
                    'toolIndex': 0,
                    'toolType': 'line',
                    'frame': 0,
                    'x1': 0,
                    'y1': 5,
                    'x2': 20,
                    'y2': 30
                },
                {
                    'toolIndex': 0,
                    'toolType': 'line',
                    'frame': 0,
                    'x1': 10,
                    'y1': 15,
                    'x2': 30,
                    'y2': 40
                },
                {
                    'toolIndex': 1,
                    'toolType': 'line',
                    'frame': 0,
                    'x1': 20,
                    'y1': 25,
                    'x2': 40,
                    'y2': 50
                },
                {
                    'toolIndex': 0,
                    'toolType': 'line',
                    'frame': 1,
                    'x1': 30,
                    'y1': 35,
                    'x2': 50,
                    'y2': 60
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
        'T0_toolIndex0_x1': [0, 10],
        'T0_toolIndex0_y1': [5, 15],
        'T0_toolIndex0_x2': [20, 30],
        'T0_toolIndex0_y2': [30, 40],
        'T0_toolIndex1_x1': [20],
        'T0_toolIndex1_y1': [25],
        'T0_toolIndex1_x2': [40],
        'T0_toolIndex1_y2': [50]
    },
    'frame1': {
        'T0_toolIndex0_x1': [30],
        'T0_toolIndex0_y1': [35],
        'T0_toolIndex0_x2': [50],
        'T0_toolIndex0_y2': [60]
    }
}

TestShapeLine_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape line V2',
    kwargs={'shape': 'line'},
    test_name='TestShapeLine_v2'
)

TestShapeLineTask_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape line V2 with task specified',
    kwargs={
        'shape': 'line',
        'task': 'T0'
    },
    test_name='TestShapeLineTask_v2'
)

TestShapeLineAllTools_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape line V2 with all tools specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeLineAllTools_v2'
)

expected_v2_0 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x1': expected_v2['frame0']['T0_toolIndex0_x1'],
        'T0_toolIndex0_y1': expected_v2['frame0']['T0_toolIndex0_y1'],
        'T0_toolIndex0_x2': expected_v2['frame0']['T0_toolIndex0_x2'],
        'T0_toolIndex0_y2': expected_v2['frame0']['T0_toolIndex0_y2']
    },
    'frame1': expected_v2['frame1']
}

TestShapeLineOneTool_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2_0,
    'Test shape line V2 with one tool specified',
    kwargs={
        'shape': 'line',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeLineOneTool_v2'
)
