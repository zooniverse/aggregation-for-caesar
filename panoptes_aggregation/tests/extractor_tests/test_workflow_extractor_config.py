import unittest
from panoptes_aggregation.extractors import workflow_extractor_config

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
                'size': 'small',
                'type': 'line'
            },
            {
                'color': '#ffff00',
                'details': [],
                'label': 'T0.tools.2.label',
                'size': 'small',
                'type': 'point'
            },
            {
                'color': '#ffffff',
                'details': [],
                'label': 'T0.tools.3.label',
                'size': 'small',
                'type': 'polygon'
            }
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

expected = {
    'T0': {
        'point_extractor': [0, 2],
        'line_extractor': [1],
        'polygon_extractor': [3]
    },
    'T1': 'question_extractor',
    'T2': 'question_extractor',
    'T3': 'survey_extractor',
    'T4': {
        'poly_line_text_extractor': [0]
    },
    'T5': {
        'line_text_extractor': [0]
    }
}


class TestWorkflowExtractorConfig(unittest.TestCase):
    def test_config(self):
        '''Test workflow auto config works'''
        result = workflow_extractor_config(tasks)
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
