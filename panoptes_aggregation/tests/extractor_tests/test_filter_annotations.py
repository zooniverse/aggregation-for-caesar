import unittest
from panoptes_aggregation.extractors import filter_annotations


class TestFilterAnnotations(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.annotation = [{
            'task': 'T0',
            'task_label': 'Please mark the galaxy centre(s) and any foreground stars you see.',
            'value': [{
                'details': [],
                'frame': 0,
                'tool': 0,
                'tool_label': 'Galaxy center',
                'x': 261,
                'y': 266
            }, {
                'details': [],
                'frame': 0,
                'tool': 2,
                'tool_label': 'Foreground Star',
                'x': 270,
                'y': 341
            }, {
                'details': [],
                'frame': 0,
                'tool': 1,
                'tool_label': 'A line',
                'x1': 714.84,
                'y1': 184.78,
                'x2': 446.35,
                'y2': 278.33
            }]
        }, {
            'task': 'T1',
            'task_label': 'A single question',
            'value': 'Yes'
        }, {
            'task': 'T2',
            'task_label': 'A multi question',
            'value': ['Blue', 'Green']
        }]
        self.config = {
            'T0': {
                'line_extractor': [1],
                'point_extractor': [0, 2]
            },
            'T1': 'question_extractor',
            'T2': 'question_extractor'
        }

    def test_filter(self):
        expected_result = {
            'line_extractor': [{
                'task': 'T0',
                'value': [{
                    'details': [],
                    'frame': 0,
                    'tool': 1,
                    'x1': 714.84,
                    'y1': 184.78,
                    'x2': 446.35,
                    'y2': 278.33
                }]
            }],
            'point_extractor': [{
                'task': 'T0',
                'value': [{
                    'details': [],
                    'frame': 0,
                    'tool': 0,
                    'x': 261,
                    'y': 266
                }, {
                    'details': [],
                    'frame': 0,
                    'tool': 2,
                    'x': 270,
                    'y': 341
                }]
            }],
            'question_extractor': [{
                'task': 'T1',
                'value': 'Yes'
            }, {
                'task': 'T2',
                'value': ['Blue', 'Green']
            }]
        }
        result = filter_annotations(self.annotation, self.config)
        self.assertDictEqual(result, expected_result)

    def test_filter_human(self):
        expected_result = {
            'line_extractor': [{
                'task': 'T0',
                'task_label': 'Please mark the galaxy centre(s) and any foreground stars you see.',
                'value': [{
                    'details': [],
                    'frame': 0,
                    'tool': 1,
                    'tool_label': 'A line',
                    'x1': 714.84,
                    'y1': 184.78,
                    'x2': 446.35,
                    'y2': 278.33
                }]
            }],
            'point_extractor': [{
                'task': 'T0',
                'task_label': 'Please mark the galaxy centre(s) and any foreground stars you see.',
                'value': [{
                    'details': [],
                    'frame': 0,
                    'tool': 0,
                    'tool_label': 'Galaxy center',
                    'x': 261,
                    'y': 266
                }, {
                    'details': [],
                    'frame': 0,
                    'tool': 2,
                    'tool_label': 'Foreground Star',
                    'x': 270,
                    'y': 341
                }]
            }],
            'question_extractor': [{
                'task': 'T1',
                'task_label': 'A single question',
                'value': 'Yes'
            }, {
                'task': 'T2',
                'task_label': 'A multi question',
                'value': ['Blue', 'Green']
            }]
        }
        result = filter_annotations(self.annotation, self.config, human=True)
        self.assertDictEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
