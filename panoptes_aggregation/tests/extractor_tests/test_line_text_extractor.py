from panoptes_aggregation import extractors
from .base_test_class import TextExtractorTest

classification = {
    'annotations': [
        {
            'task': 'T0',
            'task_label': 'draw a line under the text',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'x1': 749.7457275390625,
                    'y1': 139.9468231201172,
                    'x2': 1373.24658203125,
                    'y2': 128.85250854492188,
                    'details': [
                        {'value': "John's Island Sept 18th 1856"}
                    ],
                    'tool_label': 'line'
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'closed': True,
                    'x1': 589.2650756835938,
                    'y1': 267.0854797363281,
                    'x2': 908.8545532226562,
                    'y2': 260.9980773925781,
                    'details': [
                        {'value': 'Mr Le Blakes'}
                    ],
                    'tool_label': 'line'
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'closed': True,
                    'x1': 643.07177734375,
                    'y1': 308.71209716796875,
                    'x2': 1393.4085693359375,
                    'y2': 305.293701171875,
                    'details': [
                        {'value': 'Dear Sir I have just received'}
                    ],
                    'tool_label': 'line'
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'closed': True,
                    'x1': 587.9367065429688,
                    'y1': 131.58277893066406,
                    'x2': 1384.6763916015625,
                    'y2': 147.67852783203125,
                    'details': [
                        {'value': 'know the prospects on the next page'}
                    ],
                    'tool_label': 'line'
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
                    ],
                ]
        },
        'text': [
            ["John's Island Sept 18th 1856"],
            ['Mr Le Blakes'],
            ['Dear Sir I have just received']
        ],
        'slope': [
            -1.01939,
            -1.091213,
            -0.261027
        ]
    },
    'frame1': {
        'points': {
            'x':
                [
                    [
                        587.9367065429688,
                        1384.6763916015625
                    ]
                ],
            'y':
                [
                    [
                        131.58277893066406,
                        147.67852783203125
                    ]
                ]
        },
        'text': [
            ['know the prospects on the next page']
        ],
        'slope': [
            1.157333
        ]
    }
}

TestLineText = TextExtractorTest(
    extractors.line_text_extractor,
    classification,
    expected,
    'Test line-text extractor'
)

TestLineTextTool = TextExtractorTest(
    extractors.line_text_extractor,
    classification,
    expected,
    'Test line-text extractor with tool specified',
    kwargs={'tools': [0]}
)
