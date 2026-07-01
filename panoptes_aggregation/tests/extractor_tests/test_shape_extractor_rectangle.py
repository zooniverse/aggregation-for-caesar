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
                    'height': 30
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'width': 30,
                    'height': 40
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'width': 40,
                    'height': 50
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'width': 50,
                    'height': 60
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
        'T0_tool0_height': [30, 40],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_width': [40],
        'T0_tool1_height': [50]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_width': [50],
        'T0_tool0_height': [60]
    }
}

TestShapeRectangle = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rectangle',
    kwargs={'shape': 'rectangle'},
    test_name='TestShapeRectangle'
)

TestShapeRectangleTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rectangle with task specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0'
    },
    test_name='TestShapeRectangleTask'
)

TestShapeRectangleAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape rectangle with all tools specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeRectangleAllTools'
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_width': expected['frame0']['T0_tool0_width'],
        'T0_tool0_height': expected['frame0']['T0_tool0_height']
    },
    'frame1': expected['frame1']
}

TestShapeRectangleOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape rectangle with one tool specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeRectangleOneTool'
)

classification_v2 = {
    'annotations': [
        {
            'task': 'T0',
            'taskType': 'drawing',
            'value': [
                {
                    'toolIndex': 0,
                    'toolType': 'rectangle',
                    'frame': 0,
                    'x_center': 0,
                    'y_center': 5,
                    'width': 20,
                    'height': 30
                },
                {
                    'toolIndex': 0,
                    'toolType': 'rectangle',
                    'frame': 0,
                    'x_center': 10,
                    'y_center': 15,
                    'width': 30,
                    'height': 40
                },
                {
                    'toolIndex': 1,
                    'toolType': 'rectangle',
                    'frame': 0,
                    'x_center': 20,
                    'y_center': 25,
                    'width': 40,
                    'height': 50
                },
                {
                    'toolIndex': 0,
                    'toolType': 'rectangle',
                    'frame': 1,
                    'x_center': 30,
                    'y_center': 35,
                    'width': 50,
                    'height': 60
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
        'T0_toolIndex0_x_center': [0, 10],
        'T0_toolIndex0_y_center': [5, 15],
        'T0_toolIndex0_width': [20, 30],
        'T0_toolIndex0_height': [30, 40],
        'T0_toolIndex1_x_center': [20],
        'T0_toolIndex1_y_center': [25],
        'T0_toolIndex1_width': [40],
        'T0_toolIndex1_height': [50]
    },
    'frame1': {
        'T0_toolIndex0_x_center': [30],
        'T0_toolIndex0_y_center': [35],
        'T0_toolIndex0_width': [50],
        'T0_toolIndex0_height': [60]
    }
}

TestShapeRectangle_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape rectangle V2',
    kwargs={'shape': 'rectangle'},
    test_name='TestShapeRectangle_v2'
)

TestShapeRectangleTask_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape rectangle V2 with task specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0'
    },
    test_name='TestShapeRectangleTask_v2'
)

TestShapeRectangleAllTools_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape rectangle V2 with all tools specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeRectangleAllTools_v2'
)

expected_v2_0 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x_center': expected_v2['frame0']['T0_toolIndex0_x_center'],
        'T0_toolIndex0_y_center': expected_v2['frame0']['T0_toolIndex0_y_center'],
        'T0_toolIndex0_width': expected_v2['frame0']['T0_toolIndex0_width'],
        'T0_toolIndex0_height': expected_v2['frame0']['T0_toolIndex0_height']
    },
    'frame1': expected_v2['frame1']
}

TestShapeRectangleOneTool_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2_0,
    'Test shape rectangle V2 with one tool specified',
    kwargs={
        'shape': 'rectangle',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeRectangleOneTool_v2'
)
