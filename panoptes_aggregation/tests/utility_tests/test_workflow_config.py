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
                    },
                    {
                        'type': 'fake_task_type'
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
    },
    'T6': {
        'type': 'shortcut',
        'question': 'T6.question',
        'answers': [
            {'label': 'T6.answers.0.label'},
            {'label': 'T6.answers.1.label'}
        ]
    },
    'T7': {
        'type': 'slider',
        'instruction': 'T7.instruction',
        'max': '3',
        'min': '1.5',
        'step': '0.01'
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
                    'question_extractor',
                    None
                ]
            }
        }
    ],
    'shape_extractor_line': [
        {
            'task': 'T0',
            'tools': [1],
            'details': {},
            'shape': 'line'
        }
    ],
    'shape_extractor_rectangle': [
        {
            'task': 'T0',
            'tools': [4],
            'details': {},
            'shape': 'rectangle'
        }
    ],
    'question_extractor': [
        {'task': 'T1'},
        {'task': 'T2'},
        {'task': 'T6'}
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
    ],
    'slider_extractor': [
        {'task': 'T7'}
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
                'question_reducer',
                None
            ]
        }
    }},
    {'poly_line_text_reducer': {
        'dot_freq': 'line'
    }},
    {'question_reducer': {}},
    {'shape_reducer_dbscan': {
        'shape': 'line'
    }},
    {'shape_reducer_dbscan': {
        'shape': 'rectangle'
    }},
    {'slider_reducer': {}},
    {'survey_reducer': {}}
]


tasks_sw = {'init': {'question': 'init.question', 'type': 'single', 'answers': []}}
extractor_config_sw = {
    'question_extractor': [
        {'task': 'T0'},
        {'task': 'T3'}
    ],
    'sw_extractor': [{'task': 'T2'}],
    'sw_variant_extractor': [{'task': 'T2'}],
    'sw_graphic_extractor': [{'task': 'T2'}]
}
reducer_config_sw = [
    {'question_reducer': {}},
    {'poly_line_text_reducer': {
        'dot_freq': 'line'
    }},
    {'rectangle_reducer': {}},
    {'sw_variant_reducer': {}}
]


tasks_at = {'T0': {'type': 'annotate-task'}}
extractor_config_at = {
    'question_extractor': [
        {'task': 'T0'},
        {'task': 'T3'}
    ],
    'sw_extractor': [{'task': 'T2'}],
    'sw_graphic_extractor': [{'task': 'T2'}]
}
reducer_config_at = [
    {'question_reducer': {}},
    {'poly_line_text_reducer': {
        'dot_freq': 'line'
    }},
    {'rectangle_reducer': {}}
]


class TestWorkflowExtractorConfig(unittest.TestCase):
    def base(self, task, config, **kwargs):
        self.maxDiff = None
        result = workflow_extractor_config(task, **kwargs)
        self.assertCountEqual(result, config)
        for i in config.keys():
            with self.subTest(i=i):
                self.assertCountEqual(result[i], config[i])

    def test_config(self):
        '''Test workflow extractor auto config'''
        self.base(tasks, extractor_config, keywords=keywords)

    def test_config_sw(self):
        '''Test workflow extractor auto config for SW'''
        self.base(tasks_sw, extractor_config_sw)

    def test_config_at(self):
        '''Test workflow extractor auto config for AT'''
        self.base(tasks_at, extractor_config_at)


class TestWorkflowReducerConfig(unittest.TestCase):
    def base(self, extractor_config, reducer_config):
        self.maxDiff = None
        result = workflow_reducer_config(extractor_config)
        self.assertEqual(result, reducer_config)

    def test_config(self):
        '''Test workflow reducer auto config'''
        self.base(extractor_config, reducer_config)

    def test_config_sw(self):
        '''Test workflow reducer auto config for SW'''
        self.base(extractor_config_sw, reducer_config_sw)

    def test_config_at(self):
        '''Test workflow reducer auto config for AT'''
        self.base(extractor_config_at, reducer_config_at)


if __name__ == '__main__':
    unittest.main()
