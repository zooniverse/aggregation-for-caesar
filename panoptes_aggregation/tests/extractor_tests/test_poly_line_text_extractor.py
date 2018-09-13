from panoptes_aggregation import extractors
from .base_test_class import TextExtractorTest, TextExtractorBadKeywordTest

classification = {
    "annotations": [
        {
            "task": "T1",
            "task_label": "Mark each space between word in a line.",
            "value": [
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 749.7457275390625, "y": 139.9468231201172},
                        {"x": 891.7530517578125, "y": 133.2902374267578},
                        {"x": 1064.824462890625, "y": 133.2902374267578},
                        {"x": 1200.1751708984375, "y": 133.2902374267578},
                        {"x": 1291.1485595703125, "y": 124.41477966308594},
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
                        {"x": 686.663818359375, "y": 264.0417785644531},
                        {"x": 747.5379638671875, "y": 264.0417785644531},
                        {"x": 787.106201171875, "y": 257.9543762207031},
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
                        {"x": 790.0625610351562, "y": 308.71209716796875},
                        {"x": 902.8695068359375, "y": 303.5845031738281},
                        {"x": 996.875244140625, "y": 303.5845031738281},
                        {"x": 1123.355712890625, "y": 303.5845031738281},
                        {"x": 1224.1982421875, "y": 301.87530517578125},
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
                        {"x": 716.7026977539062, "y": 131.58277893066406},
                        {"x": 795.5718994140625, "y": 126.7540512084961},
                        {"x": 1004.8167114257812, "y": 138.0210723876953},
                        {"x": 1091.7337646484375, "y": 136.4114990234375},
                        {"x": 1167.3837890625, "y": 139.6306610107422},
                        {"x": 1275.225341796875, "y": 139.6306610107422},
                        {"x": 1384.6763916015625, "y": 147.67852783203125}
                    ],
                    "details": [
                        {"value": "know the prospects on the next page"}
                    ],
                    "tool_label": "Tool name"
                }
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
                        891.7530517578125,
                        1064.824462890625,
                        1200.1751708984375,
                        1291.1485595703125,
                        1373.24658203125
                    ],
                    [
                        643.07177734375,
                        790.0625610351562,
                        902.8695068359375,
                        996.875244140625,
                        1123.355712890625,
                        1224.1982421875,
                        1393.4085693359375
                    ]
                ],
            'y':
                [
                    [
                        139.9468231201172,
                        133.2902374267578,
                        133.2902374267578,
                        133.2902374267578,
                        124.41477966308594,
                        128.85250854492188
                    ],
                    [
                        308.71209716796875,
                        308.71209716796875,
                        303.5845031738281,
                        303.5845031738281,
                        303.5845031738281,
                        301.87530517578125,
                        305.293701171875
                    ]
                ]
        },
        'text': [
            ["John's", 'Island', 'Sept', '18th', '1856'],
            ['Dear', 'Sir', 'I', 'have', 'just', 'received']
        ],
        'slope': [
            -1.0475230663632435,
            -0.39003195214578423
        ]
    },
    'frame1': {
        'points': {
            'x':
                [
                    [
                        587.9367065429688,
                        716.7026977539062,
                        795.5718994140625,
                        1004.8167114257812,
                        1091.7337646484375,
                        1167.3837890625,
                        1275.225341796875,
                        1384.6763916015625
                    ]
                ],
            'y':
                [
                    [
                        131.58277893066406,
                        131.58277893066406,
                        126.7540512084961,
                        138.0210723876953,
                        136.4114990234375,
                        139.6306610107422,
                        139.6306610107422,
                        147.67852783203125
                    ]
                ]
        },
        'text': [
            ['know', 'the', 'prospects', 'on', 'the', 'next', 'page']
        ],
        'slope': [
            1.1519519690072122
        ]
    }
}

TestPolyLineText = TextExtractorTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by word'
)

TestPolyLineTextTool = TextExtractorTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by word with tool specified',
    kwargs={'tools': [0]}
)

TestPolyLineTextBadKeyword = TextExtractorBadKeywordTest(
    extractors.poly_line_text_extractor,
    classification,
    expected,
    'Test poly-line-text extractor by word with bad keyword'
)
