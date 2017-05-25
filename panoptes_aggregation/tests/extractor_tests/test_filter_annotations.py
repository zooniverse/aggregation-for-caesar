import unittest
from panoptes_aggregation.extractors import filter_annotations


class TestFilterAnnotations(unittest.TestCase):
    def setUp(self):
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
        }]
        self.config = {'T0': {'line_extractor': [1], 'point_extractor': [0, 2]}}
        self.expected_result = {
            'line_extractor': {
                'task': 'T0',
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
            },
            'point_extractor': {
                'task': 'T0',
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
            }
        }

    def test_filter(self):
        result = filter_annotations(self.annotation, self.config)
        self.assertDictEqual(result, self.expected_result)


if __name__ == '__main__':
    unittest.main()
