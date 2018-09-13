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
                    'y': 0,
                    'width': 5,
                    'height': 10,
                    'details': [
                        {'value': 0},
                        {'value': [1, 0]},
                        {'value': [
                            {
                                'value': 'Option 1',
                                'option': True
                            },
                            {
                                'value': 'Option 2',
                                'option': True
                            },
                            {
                                'value': None,
                                'option': False
                            }
                        ]},
                        {'not-supported-subtask': 1}
                    ]
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 100,
                    'y': 105,
                    'width': 50,
                    'height': 100,
                    'details': [
                        {'value': 1},
                        {'value': [0]},
                        {'value': [
                            {
                                'value': 'Option 3',
                                'option': True
                            },
                            {
                                'value': 'Option 4',
                                'option': True
                            },
                            {
                                'value': 'Option 5',
                                'option': True
                            }
                        ]},
                        {'not-supported-subtask': 1}
                    ]
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 500,
                    'y': 500,
                    'width': 10,
                    'height': 20,
                    'details': []
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T0_tool0_x': [0, 100],
        'T0_tool0_y': [0, 105],
        'T0_tool0_width': [5, 50],
        'T0_tool0_height': [10, 100],
        'T0_tool0_details': [
            [
                {'0': 1},
                {'1': 1, '0': 1},
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'None': 1}
                ]},
                'No extractor for this subtask type'
            ],
            [
                {'1': 1},
                {'0': 1},
                {'value': [
                    {'option-3': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]},
                'No extractor for this subtask type'
            ]
        ],
        'T0_tool1_x': [500],
        'T0_tool1_y': [500],
        'T0_tool1_width': [10],
        'T0_tool1_height': [20],
    }
}

TestSubtask = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test subtask extraction',
    kwargs={
        'details': {
            'T0_tool0': [
                'question_extractor',
                'question_extractor',
                'dropdown_extractor',
                None
            ]
        }
    }
)

TestSubtaskTask = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test subtask extraction with task specified',
    kwargs={
        'task': 'T0',
        'details': {
            'T0_tool0': [
                'question_extractor',
                'question_extractor',
                'dropdown_extractor',
                None
            ]
        }
    }
)

TestSubtaskAllTools = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected,
    'Test subtask extraction with all tools specified',
    kwargs={
        'tools': [0, 1],
        'details': {
            'T0_tool0': [
                'question_extractor',
                'question_extractor',
                'dropdown_extractor',
                None
            ]
        }
    }
)

expected_0 = {
    'frame0': {
        'T0_tool0_x': [0, 100],
        'T0_tool0_y': [0, 105],
        'T0_tool0_width': [5, 50],
        'T0_tool0_height': [10, 100],
        'T0_tool0_details': [
            [
                {'0': 1},
                {'1': 1, '0': 1},
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'None': 1}
                ]},
                'No extractor for this subtask type'
            ],
            [
                {'1': 1},
                {'0': 1},
                {'value': [
                    {'option-3': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]},
                'No extractor for this subtask type'
            ]
        ]
    }
}

TestSubtaskOneTool = ExtractorTest(
    extractors.rectangle_extractor,
    classification,
    expected_0,
    'Test subtask extraction with one tool specified',
    kwargs={
        'tools': [0],
        'details': {
            'T0_tool0': [
                'question_extractor',
                'question_extractor',
                'dropdown_extractor',
                None
            ]
        }
    }
)
