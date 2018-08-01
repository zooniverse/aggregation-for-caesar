from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [{
        "task": "T0",
        "value": [
            {
                "frame": 0,
                "tool": 0,
                "y": 202.87478637695312,
                "details": [],
                "x": 452.18341064453125
            },
            {
                "frame": 0,
                "tool": 1,
                "y": 583.4398803710938,
                "details": [],
                "x": 404.61279296875
            },
            {
                "frame": 0,
                "tool": 0,
                "y": 306.410888671875,
                "details": [],
                "x": 190.54489135742188
            },
            {
                "frame": 0,
                "tool": 1,
                "y": 568.0493774414062,
                "details": [],
                "x": 422.8015441894531
            },
            {
                "frame": 0,
                "tool": 1,
                "y": 612.82177734375,
                "details": [],
                "x": 435.3937683105469
            },
            {
                "frame": 0,
                "tool": 1,
                "y": 617.0191650390625,
                "details": [],
                "x": 371.03350830078125
            },
            {
                "frame": 0,
                "tool": 0,
                "y": 235.054931640625,
                "details": [],
                "x": 408.8101806640625
            },
            {
                "frame": 0,
                "tool": 0,
                "y": 158.1024169921875,
                "details": [],
                "x": 411.60845947265625
            },
            {
                "frame": 0,
                "tool": 0,
                "y": 180.4886016845703,
                "details": [],
                "x": 482.96441650390625
            }
        ]
    }]
}

expected = {
    'T0_tool0_x': [
        452.18341064453125,
        190.54489135742188,
        408.8101806640625,
        411.60845947265625,
        482.96441650390625
    ],
    'T0_tool0_y': [
        202.87478637695312,
        306.410888671875,
        235.054931640625,
        158.1024169921875,
        180.4886016845703
    ],
    'T0_tool1_x': [
        404.61279296875,
        422.8015441894531,
        435.3937683105469,
        371.03350830078125
    ],
    'T0_tool1_y': [
        583.4398803710938,
        568.0493774414062,
        612.82177734375,
        617.0191650390625
    ]
}

TestPoint = ExtractorTest(
    extractors.point_extractor,
    classification,
    expected,
    'Test point'
)

TestPointTask = ExtractorTest(
    extractors.point_extractor,
    classification,
    expected,
    'Test point with task specified',
    kwargs={'task': 'T0'}
)

TestPointAllTools = ExtractorTest(
    extractors.point_extractor,
    classification,
    expected,
    'Test point with all tools specified',
    kwargs={
        'task': 'T0',
        'tools': [0, 1]
    }
)

expected_0 = {
    'T0_tool0_x': expected['T0_tool0_x'],
    'T0_tool0_y': expected['T0_tool0_y']
}

TestPointOneTool = ExtractorTest(
    extractors.point_extractor,
    classification,
    expected_0,
    'Test point with one tool specified',
    kwargs={
        'task': 'T0',
        'tools': [0]
    }
)
