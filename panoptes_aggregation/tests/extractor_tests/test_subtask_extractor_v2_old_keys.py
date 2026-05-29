from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [{
        "task": "T0",
        "taskType": "drawing",
        "value": [
            {
                "toolIndex": 0,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 2.5,
                "y_center": 5,
                "width": 5,
                "height": 10,
                "details": [
                    {"task": "T0.0.0"},
                    {"task": "T0.0.1"}
                ]
            }, {
                "toolIndex": 0,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 125,
                "y_center": 155,
                "width": 50,
                "height": 100,
                "details": [
                    {"task": "T0.0.0"},
                    {"task": "T0.0.1"}
                ]
            }, {
                "toolIndex": 1,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 505,
                "y_center": 510,
                "width": 10,
                "height": 20,
                "details": []
            }
        ]
    }, {
        "task": "T0.0.0",
        "taskType": "single",
        "markIndex": 0,
        "value": 0
    }, {
        "task": "T0.0.0",
        "taskType": "single",
        "markIndex": 1,
        "value": 1
    }, {
        "task": "T0.0.1",
        "taskType": "single",
        "markIndex": 0,
        "value": 1
    }, {
        "task": "T0.0.1",
        "taskType": "single",
        "markIndex": 1,
        "value": 2
    }], 
    "metadata": {
        "classifier_version": "2.0"
    }
}

expected = {
    "classifier_version": "2.0",
    "frame0": {
        "T0_tool0_x_center": [2.5, 125],
        "T0_tool0_y_center": [5, 155],
        "T0_tool0_width": [5, 50],
        "T0_tool0_height": [10, 100],
        "T0_toolIndex0_subtask0": [{"0": 1}, {"1": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
        "T0_tool1_x_center": [505],
        "T0_tool1_y_center": [510],
        "T0_tool1_width": [10],
        "T0_tool1_height": [20],
    }
}

TestSubtaskV2_V1tools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test subtask v2.0 extraction',
    kwargs={
        'shape': 'rectangle',
        'use_v1_keys': True,
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'question_extractor'
        }
    },
    test_name='TestSubtaskV2_V1tools'
)
