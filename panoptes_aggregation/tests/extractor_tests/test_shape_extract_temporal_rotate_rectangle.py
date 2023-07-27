from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [
        {
            "task": "T0",
            "value": [
                {
                    "angle": 0.3917729405940556,
                    "details": [],
                    "displayTime": 0.361,
                    "displayTimeStamp": "01:444",
                    "frame": 0,
                    "height": 471.2629543273978,
                    "toolIndex": 2,
                    "toolType": "temporalRotateRectangle",
                    "tool_label": None,
                    "width": 87.22731096735055,
                    "x_center": 214.2397181088975,
                    "y_center": 441.21555066032676,
                },
            ],
        }
    ]
}


expected = {
    "frame0": {
        "T0_toolIndex2_angle": [0.3917729405940556],
        "T0_toolIndex2_displayTime": [0.361],
        "T0_toolIndex2_height": [471.2629543273978],
        "T0_toolIndex2_width": [87.22731096735055],
        "T0_toolIndex2_x_center": [214.2397181088975],
        "T0_toolIndex2_y_center": [441.21555066032676],
    },
}

TestShapeRotateRectangle = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape temporalRotateRectangle',
    kwargs={'shape': 'temporalRotateRectangle'},
    test_name='TestShapeTemporalRotateRectangle'
)
