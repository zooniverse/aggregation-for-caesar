from panoptes_aggregation import extractors
from .base_test_class import TextExtractorTest, TextExtractorBadKeywordTest

classification = {
    "gold_standard": True,
    "annotations": [
        {
            "task": "T1",
            "task_label": "Mark each line.",
            "value": [
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 749.7457275390625, "y": 139.9468231201172},
                        {"x": 1373.24658203125, "y": 128.85250854492188}
                    ],
                    "details": [
                        {"value": "John's Island Sept 18th 1856"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 589.2650756835938, "y": 267.0854797363281},
                        {"x": 908.8545532226562, "y": 260.9980773925781}
                    ],
                    "details": [
                        {"value": "Mr Le Blakes"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 643.07177734375, "y": 308.71209716796875},
                        {"x": 1393.4085693359375, "y": 305.293701171875}
                    ],
                    "details": [
                        {"value": "Dear Sir I have just received"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 587.9367065429688, "y": 131.58277893066406},
                        {"x": 1384.6763916015625, "y": 147.67852783203125}
                    ],
                    "details": [
                        {"value": "know the prospects on the next page"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 600, "y": 0},
                        {"x": 600, "y": 100}
                    ],
                    "details": [
                        {"value": "This is vertical text"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 800, "y": 900},
                        {"x": 800, "y": 900}
                    ],
                    "details": [
                        {"value": "This line has 0 length"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 0, "y": 600},
                        {"x": 100, "y": 600}
                    ],
                    "details": [
                        {"value": "This is horizontal text"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 100, "y": 600},
                        {"x": 0, "y": 600}
                    ],
                    "details": [
                        {"value": "This is upsidedown text"}
                    ],
                    "tool_label": "Tool name"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 600, "y": 100},
                        {"x": 600, "y": 0}
                    ],
                    "details": [
                        {"value": "This is upsidedown and vertical text"}
                    ],
                    "tool_label": "Tool name"
                },
            ]
        }
    ]
}

expected = {
    'frame0': {
        'points': {
            'x':
                [
                    [
                        749.7457275390625,
                        1373.24658203125
                    ],
                    [
                        589.2650756835938,
                        908.8545532226562
                    ],
                    [
                        643.07177734375,
                        1393.4085693359375
                    ]
                ],
            'y':
                [
                    [
                        139.9468231201172,
                        128.85250854492188
                    ],
                    [
                        267.0854797363281,
                        260.9980773925781
                    ],
                    [
                        308.71209716796875,
                        305.293701171875
                    ]
                ]
        },
        'text': [
            ["John's Island Sept 18th 1856"],
            ["Mr Le Blakes"],
            ['Dear Sir I have just received']
        ],
        'slope': [
            -1.01939,
            -1.091213,
            -0.261027
        ],
        'gold_standard': True
    },
    'frame1': {
        'points': {
            'x':
                [
                    [
                        587.9367065429688,
                        1384.6763916015625
                    ],
                    [
                        600,
                        600
                    ],
                    [
                        800,
                        800
                    ],
                    [
                        0,
                        100
                    ],
                    [
                        100,
                        0
                    ],
                    [
                        600,
                        600
                    ]
                ],
            'y':
                [
                    [
                        131.58277893066406,
                        147.67852783203125
                    ],
                    [
                        0,
                        100
                    ],
                    [
                        900,
                        900
                    ],
                    [
                        600,
                        600
                    ],
                    [
                        600,
                        600
                    ],
                    [
                        100,
                        0
                    ]
                ]
        },
        'text': [
            ['know the prospects on the next page'],
            ['This is vertical text'],
            ['This line has 0 length'],
            ['This is horizontal text'],
            ['This is upsidedown text'],
            ['This is upsidedown and vertical text']
        ],
        'slope': [
            1.157333,
            90,
            0,
            0,
            180,
            -90
        ],
        'gold_standard': True
    }
}

TestPolyLineTextByLine = TextExtractorTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by line',
    kwargs={'dot_freq': 'line'},
    test_name='TestPolyLineTextByLine'
)

TestPolyLineTextByLineTool = TextExtractorTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by line with tool specified',
    kwargs={'dot_freq': 'line', 'tools': [0]},
    test_name='TestPolyLineTextByLineTool'
)

TestPolyLineTextByLineBadKeyword = TextExtractorBadKeywordTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by line with bad keyword',
    test_name='TestPolyLineTextByLineBadKeyword'
)
