import unittest
from panoptes_aggregation.workflow_config import workflow_extractor_config, workflow_reducer_config


tasks = {
    'T0': {
        'enableHidePrevMarks': True,
        'help': 'T0.help',
        'instruction': 'T0.instruction',
        'next': 'T1',
        'tools': [
            {
                'color': '#00ffff',
                'details': [],
                'label': 'T0.tools.0.label',
                'size': 'small',
                'type': 'point'
            },
            {
                'color': '#ff0000',
                'details': [],
                'label': 'T0.tools.1.label',
                'type': 'line'
            },
            {
                'color': '#ffff00',
                'details': [
                    {
                        'type': 'single',
                        'answers': [
                            {'label': 'T0.tools.2.detals.0.answers.0.label'},
                            {'label': 'T0.tools.2.detals.0.answers.1.label'}
                        ],
                        'question': 'T0.tools.2.detals.0.question'
                    },
                    {
                        'type': 'multiple',
                        'answers': [
                            {'label': 'T0.tools.2.detals.1.answers.0.label'},
                            {'label': 'T0.tools.2.detals.1.answers.1.label'}
                        ],
                        'question': 'T0.tools.2.detals.1.question'
                    }
                ],
                'label': 'T0.tools.2.label',
                'size': 'small',
                'type': 'point'
            },
            {
                'color': '#ffffff',
                'details': [],
                'label': 'T0.tools.3.label',
                'type': 'polygon'
            },
            {
                'color': '#ff00ff',
                'details': [],
                'label': 'T0.tools.4.label',
                'type': 'rectangle'
            },
        ],
        'type': 'drawing'
    },
    'T1': {
        'help': 'T1.help',
        'type': 'single',
        'answers': [
            {'next': 'T2', 'label': 'T1.answers.0.label'},
            {'next': 'T2', 'label': 'T1.answers.1.label'},
            {'label': 'T1.answers.2.label'}
        ],
        'question': 'T1.question',
        'required': True
    },
    'T2': {
        'help': 'T2.help',
        'type': 'multiple',
        'answers': [
            {'label': 'T2.answers.0.label'},
            {'label': 'T2.answers.1.label'},
            {'label': 'T2.answers.2.label'}
        ],
        'question': 'T2.question'
    },
    'T3': {
        'type': 'survey',
        'help': 'T3.help'
    },
    'T4': {
        'help': 'T4.help',
        'type': 'drawing',
        'tools': [
            {
                'type': 'polygon',
                'color': '#00ff00',
                'label': 'T4.tools.0.label',
                'details': [
                    {
                        'help':
                        'T4.tools.0.details.0.help',
                        'type': 'text',
                        'instruction': 'T4.tools.0.details.0.instruction'
                    }
                ]
            }
        ],
        'instruction': 'T4.instruction'
    },
    'T5': {
        'help': 'T5.help',
        'type': 'drawing',
        'tools': [
            {
                'type': 'line',
                'color': '#ff0000',
                'label': 'T5.tools.0.label',
                'details': [
                    {
                        'help': 'T5.tools.0.details.0.help',
                        'type': 'text',
                        'instruction': 'T5.tools.0.details.0.instruction'
                    }
                ]
            }
        ],
        'instruction': 'T5.instruction'
    }
}

keywords = {
    'T4': {'dot_freq': 'line'},
    'T5': {'dot_freq': 'word'}
}

extractor_config = {
    'point_extractor_by_frame': [
        {
            'task': 'T0',
            'tools': [0, 2],
            'details': {
                'T0_tool2': [
                    'question_extractor',
                    'question_extractor'
                ]
            }
        }
    ],
    'rectangle_extractor': [
        {
            'task': 'T0',
            'tools': [4],
            'details': {}
        }
    ],
    'question_extractor': [
        {'task': 'T1'},
        {'task': 'T2'}
    ],
    'survey_extractor': [
        {'task': 'T3'}
    ],
    'poly_line_text_extractor': [
        {
            'task': 'T4',
            'dot_freq': 'line'
        }
    ],
    'line_text_extractor': [
        {
            'task': 'T5',
            'dot_freq': 'word'
        }
    ]
}

reducer_config = [
    {'poly_line_text_reducer': {
        'dot_freq': 'word'
    }},
    {'point_reducer_dbscan': {
        'details': {
            'T0_tool2': [
                'question_reducer',
                'question_reducer'
            ]
        }
    }},
    {'poly_line_text_reducer': {
        'dot_freq': 'line'
    }},
    {'question_reducer': {}},
    {'rectangle_reducer': {}},
    {'survey_reducer': {}},
]


class TestWorkflowExtractorConfig(unittest.TestCase):
    def test_config(self):
        '''Test workflow extractor auto config'''
        self.maxDiff = None
        result = workflow_extractor_config(tasks, keywords=keywords)
        self.assertCountEqual(result, extractor_config)
        for i in extractor_config.keys():
            with self.subTest(i=i):
                self.assertCountEqual(result[i], extractor_config[i])


class TestWorkflowReducerConfig(unittest.TestCase):
    def test_config(self):
        '''Test workflow reducer auto config'''
        self.maxDiff = None
        result = workflow_reducer_config(extractor_config)
        self.assertEqual(result, reducer_config)


if __name__ == '__main__':
    unittest.main()
