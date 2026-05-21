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
                    'r': 20
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 10,
                    'y': 15,
                    'r': 30
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'r': 40
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 30,
                    'y': 35,
                    'r': 50
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 10],
        'T0_tool0_y': [5, 15],
        'T0_tool0_r': [20, 30],
        'T0_tool1_x': [20],
        'T0_tool1_y': [25],
        'T0_tool1_r': [40]
    },
    'frame1': {
        'T0_tool0_x': [30],
        'T0_tool0_y': [35],
        'T0_tool0_r': [50]
    }
}

TestShapeCircle = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle',
    kwargs={'shape': 'circle'},
    test_name='TestShapeCircle'
)

TestShapeCircleTask = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle with task specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0'
    },
    test_name='TestShapeCircleTask'
)

TestShapeCircleAllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape circle with all tools specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeCircleAllTools'
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': expected['frame0']['T0_tool0_x'],
        'T0_tool0_y': expected['frame0']['T0_tool0_y'],
        'T0_tool0_r': expected['frame0']['T0_tool0_r']
    },
    'frame1': expected['frame1']
}

TestShapeCircleOneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test shape circle with one tool specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeCircleOneTool'
)


classification_v2 = {
    'annotations': [
        {
            'task': 'T0',
            'value': [
                {
                    'toolIndex': 0,
                    'frame': 0,
                    'x_center': 0,
                    'y_center': 5,
                    'r': 20,
                    'angle': 30
                },
                {
                    'toolIndex': 0,
                    'frame': 0,
                    'x_center': 10,
                    'y_center': 15,
                    'r': 30,
                    'angle': 40
                },
                {
                    'toolIndex': 1,
                    'frame': 0,
                    'x_center': 20,
                    'y_center': 25,
                    'r': 40,
                    'angle': 50
                },
                {
                    'toolIndex': 0,
                    'frame': 1,
                    'x_center': 30,
                    'y_center': 35,
                    'r': 50,
                    'angle': 60
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
        'T0_toolIndex0_r': [20, 30],
        'T0_toolIndex1_x_center': [20],
        'T0_toolIndex1_y_center': [25],
        'T0_toolIndex1_r': [40]
    },
    'frame1': {
        'T0_toolIndex0_x_center': [30],
        'T0_toolIndex0_y_center': [35],
        'T0_toolIndex0_r': [50]
    }
}

TestShapeCircle_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape circle  V2',
    kwargs={'shape': 'circle'},
    test_name='TestShapeCircle_v2'
)

TestShapeCircleTask_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape circle V2 with task specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0'
    },
    test_name='TestShapeCircleTask_v2'
)

TestShapeCircleAllTools_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2,
    'Test shape circle V2 with all tools specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0, 1]
    },
    test_name='TestShapeCircleAllTools_v2'
)

expected_v2_0 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x_center': expected_v2['frame0']['T0_toolIndex0_x_center'],
        'T0_toolIndex0_y_center': expected_v2['frame0']['T0_toolIndex0_y_center'],
        'T0_toolIndex0_r': expected_v2['frame0']['T0_toolIndex0_r']
    },
    'frame1': expected_v2['frame1']
}

TestShapeCircleOneTool_v2 = ExtractorTest(
    extractors.shape_extractor,
    classification_v2,
    expected_v2_0,
    'Test shape circle V2 with one tool specified',
    kwargs={
        'shape': 'circle',
        'task': 'T0',
        'tools': [0]
    },
    test_name='TestShapeCircleOneTool_v2'
)
