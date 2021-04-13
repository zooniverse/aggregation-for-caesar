import unittest
from panoptes_aggregation.workflow_config import workflow_extractor_config, workflow_reducer_config

tasks = {
    'T0': {
        'help': 'T0.help',
        'next': 'T6',
        'type': 'combo',
        'tasks': ['T1', 'T2', 'T3', 'T4', 'T5']
    },
    'T1': {
        'help': 'T1.help',
        'type': 'text',
        'instruction': 'T1.instruction'
    },
    'T2': {
        'help': 'T1.help',
        'type': 'text',
        'instruction': 'T1.instruction'
    },
    'T3': {
        'help': 'T1.help',
        'type': 'text',
        'instruction': 'T1.instruction'
    },
    'T4': {
        'help': 'T1.help',
        'type': 'text',
        'instruction': 'T1.instruction'
    },
    'T5': {
        'help': 'T1.help',
        'type': 'text',
        'instruction': 'T1.instruction'
    }
}

extractor_config = {
    'text_extractor': [
        {'task': 'T1'},
        {'task': 'T2'},
        {'task': 'T3'},
        {'task': 'T4'},
        {'task': 'T5'}
    ]
}

reducer_config = [
    {'text_reducer': {}}
]


class TestWorkflowConfigCombo2(unittest.TestCase):
    maxDiff = None

    def test_extractor_config(self):
        '''Test workflow extractor config for combo task in classifier version 2.0'''
        result = workflow_extractor_config(tasks)
        self.assertDictEqual(result, extractor_config)

    def test_reducer_config(self):
        '''Test workflow reducer config for combo task in classifier version 2.0'''
        result = workflow_reducer_config(extractor_config)
        self.assertEqual(result, reducer_config)


if __name__ == '__main__':
    unittest.main()
