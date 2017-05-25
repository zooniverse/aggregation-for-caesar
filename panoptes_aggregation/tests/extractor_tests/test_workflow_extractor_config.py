import unittest
from panoptes_aggregation.extractors import workflow_extractor_config


class TestWorkflowExtractorConfig(unittest.TestCase):
    def setUp(self):
        self.tasks = {
            'T0': {
                'enableHidePrevMarks': True,
                'help': 'T0.help',
                'instruction': 'T0.instruction',
                'next': 'T1',
                'tools': [{'color': '#00ffff',
                           'details': [],
                           'label': 'T0.tools.0.label',
                           'size': 'small',
                           'type': 'point'},
                          {'color': '#ff0000',
                           'details': [],
                           'label': 'T0.tools.1.label',
                           'size': 'small',
                           'type': 'line'},
                          {'color': '#ffff00',
                           'details': [],
                           'label': 'T0.tools.2.label',
                           'size': 'small',
                           'type': 'point'}],
                'type': 'drawing'
            }
        }
        self.expected_result = {
            'T0': {
                'point_extractor': [0, 2],
                'line_extractor': [1]
            }
        }

    def test_config(self):
        result = workflow_extractor_config(self.tasks)
        self.assertDictEqual(result, self.expected_result)


if __name__ == '__main__':
    unittest.main()
