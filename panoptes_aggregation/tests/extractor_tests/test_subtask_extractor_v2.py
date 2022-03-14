from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [
        {
            'task': 'T0',
            'taskType': 'drawing',
            'value': [
                {
                    'frame': 0,
                    'toolIndex': 0,
                    'toolType': 'point',
                    'x': 452.18341064453125,
                    'y': 202.87478637695312,
                    'details': [
                        {'task': 'T0.0.0'},
                        {'task': 'T0.0.1'}
                    ]
                },
                {
                    'frame': 0,
                    'toolIndex': 0,
                    'toolType': 'point',
                    'x': 374.23454574576868,
                    'y': 455.23453656547428,
                    'details': [
                        {'task': 'T0.0.0'},
                        {'task': 'T0.0.1'}
                    ]
                },
                {
                    'frame': 0,
                    'toolIndex': 1,
                    'toolType': 'point',
                    'x': 404.61279296875,
                    'y': 583.4398803710938,
                    'details': [
                        {'task': 'T0.1.0'},
                        {'task': 'T0.1.1'}
                    ]
                }
            ]
        },
        {
            'task': 'T0.0.0',
            'taskType': 'single',
            'markIndex': 0,
            'value': 0
        },
        {
            'task': 'T0.0.1',
            'taskType': 'dropdown',
            'markIndex': 0,
            'value': [
                {'value': 'option-1'},
                {'value': 'option-2'},
                {'value': None}
            ]
        },
        {
            'task': 'T0.0.0',
            'taskType': 'single',
            'markIndex': 1,
            'value': 1
        },
        {
            'task': 'T0.0.1',
            'taskType': 'dropdown',
            'markIndex': 1,
            'value': [
                {'value': 'option-3'},
                {'value': 'option-4'},
                {'value': 'option-5'}
            ]
        },
        {
            'task': 'T0.1.0',
            'markIndex': 2,
            'taskType': 'single',
            'value': 1
        },
        {
            'task': 'T0.1.1',
            'markIndex': 2,
            'taskType': 'dropdown',
            'value': [
                {'value': 'option-3'},
                {'value': 'option-4'},
                {'value': 'option-5'}
            ]
        }
    ],
    'metadata': {
        'classifier_version': '2.0'
    }
}

expected = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [
            452.18341064453125,
            374.23454574576868
        ],
        'T0_toolIndex0_y': [
            202.87478637695312,
            455.23453656547428
        ],
        'T0_toolIndex0_subtask0': [
            {'0': 1},
            {'1': 1}
        ],
        'T0_toolIndex0_subtask1': [
            {'value': [
                {'option-1': 1},
                {'option-2': 1},
                {'None': 1}
            ]},
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]}
        ],
        'T0_toolIndex1_x': [404.61279296875],
        'T0_toolIndex1_y': [583.4398803710938],
        'T0_toolIndex1_subtask0': [
            {'1': 1}
        ],
        'T0_toolIndex1_subtask1': [
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]}
        ]
    }
}

TestSubtaskV2 = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test subtask v2.0 extraction',
    kwargs={
        'shape': 'point',
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'dropdown_extractor',
            'T0_toolIndex1_subtask0': 'question_extractor',
            'T0_toolIndex1_subtask1': 'dropdown_extractor'
        }
    },
    test_name='TestSubtaskV2'
)

TestSubtaskV2Task = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test subtask v2.0 extraction with task specified',
    kwargs={
        'task': 'T0',
        'shape': 'point',
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'dropdown_extractor',
            'T0_toolIndex1_subtask0': 'question_extractor',
            'T0_toolIndex1_subtask1': 'dropdown_extractor'
        }
    },
    test_name='TestSubtaskV2Task'
)

TestSubtaskV2AllTools = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test subtask v2.0 extraction with all tools specified',
    kwargs={
        'tools': [0, 1],
        'shape': 'point',
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'dropdown_extractor',
            'T0_toolIndex1_subtask0': 'question_extractor',
            'T0_toolIndex1_subtask1': 'dropdown_extractor'
        }
    },
    test_name='TestSubtaskV2AllTools'
)

expected_0 = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [
            452.18341064453125,
            374.23454574576868
        ],
        'T0_toolIndex0_y': [
            202.87478637695312,
            455.23453656547428
        ],
        'T0_toolIndex0_subtask0': [
            {'0': 1},
            {'1': 1}
        ],
        'T0_toolIndex0_subtask1': [
            {'value': [
                {'option-1': 1},
                {'option-2': 1},
                {'None': 1}
            ]},
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]}
        ]
    }
}

TestSubtaskV2OneTool = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_0,
    'Test subtask v2.0 extraction with one tool specified',
    kwargs={
        'tools': [0],
        'shape': 'point',
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'dropdown_extractor'
        }
    },
    test_name='TestSubtaskV2OneTool'
)

expected_no_sub = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [
            452.18341064453125,
            374.23454574576868
        ],
        'T0_toolIndex0_y': [
            202.87478637695312,
            455.23453656547428
        ],
        'T0_toolIndex1_x': [404.61279296875],
        'T0_toolIndex1_y': [583.4398803710938],
    }
}

TestSubtaskV2NoSub = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_no_sub,
    'Test subtask v2.0 extraction with no subtask extractors configured',
    kwargs={'shape': 'point'},
    test_name='TestSubtaskV2NoSub'
)

expected_one_sub = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_x': [
            452.18341064453125,
            374.23454574576868
        ],
        'T0_toolIndex0_y': [
            202.87478637695312,
            455.23453656547428
        ],
        'T0_toolIndex0_subtask0': [
            {'0': 1},
            {'1': 1}
        ],
        'T0_toolIndex0_subtask1': [
            {'value': [
                {'option-1': 1},
                {'option-2': 1},
                {'None': 1}
            ]},
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]}
        ],
        'T0_toolIndex1_x': [404.61279296875],
        'T0_toolIndex1_y': [583.4398803710938],
    }
}

TestSubtaskV2OneSub = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected_one_sub,
    'Test subtask v2.0 extraction with one subtask extractors configured',
    kwargs={
        'shape': 'point',
        'details': {
            'T0_toolIndex0_subtask0': 'question_extractor',
            'T0_toolIndex0_subtask1': 'dropdown_extractor'
        }
    },
    test_name='TestSubtaskV2OneSub'
)
