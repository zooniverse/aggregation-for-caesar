import unittest
import flask
import json
from panoptes_aggregation.reducers.poly_line_text_reducer import process_data, poly_line_text_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

extracted_data = [
    {
        'frame0': {
            'points': {'x': [5, 12], 'y': [1, 1.2]},
            'text': ['b', '7']
        },
        'frame1': {
            'points': {'x': [1, 8], 'y': [1, 1.1]},
            'text': ['page', '2']
        }
    },
    {
        'frame0': {
            'points': {'x': [5.5, 13], 'y': [1.5, 1.4]},
            'text': ['B', '7']
        }
    },
    {
        'frame0': {
            'points': {'x': [4, 11], 'y': [1.1, 0.9]},
            'text': ['ZZZ', '[unclear]7[/unclear]']
        },
        'frame1': {
            'points': {'x': [1.1, 8.1], 'y': [0.9, 1]},
            'text': ['page', '2']
        }
    },
    {
        'frame0': {
            'points': {'x': [8, 15, 32], 'y': [4, 4.1, 4]},
            'text': ['a', 'page', 'of']
        },
        'frame1': {
            'points': {'x': [1.05, 7.9], 'y': [0.8, 0.9]},
            'text': ['page', '2']
        }
    },
    {
        'frame0': {
            'points': {'x': [8, 16, 33], 'y': [4.3, 4.3, 4.1]},
            'text': ['A', 'page', 'of']
        }
    },
    {
        'frame0': {
            'points': {'x': [7.5, 14, 35, 72], 'y': [4.7, 4.8, 4.7, 5]},
            'text': ['c', 'page', 'of', 'text']
        }
    }
]

processed_data = {
    'frame0': {
        'loc': [
            (5, 1),
            (12, 1.2),
            (5.5, 1.5),
            (13, 1.4),
            (4, 1.1),
            (11, 0.9),
            (8, 4),
            (15, 4.1),
            (32, 4),
            (8, 4.3),
            (16, 4.3),
            (33, 4.1),
            (7.5, 4.7),
            (14, 4.8),
            (35, 4.7),
            (72, 5)
        ],
        'text': [
            'b',
            '7',
            'B',
            '7',
            'ZZZ',
            '[unclear]7[/unclear]',
            'a',
            'page',
            'of',
            'A',
            'page',
            'of',
            'c',
            'page',
            'of',
            'text'
        ]
    },
    'frame1': {
        'loc': [
            (1, 1),
            (8, 1.1),
            (1.1, 0.9),
            (8.1, 1),
            (1.05, 0.8),
            (7.9, 0.9)
        ],
        'text': [
            'page',
            '2',
            'page',
            '2',
            'page',
            '2'
        ]
    }
}

reduced_data = {
    'frame0': {
        'clusters_x': [
            4.833333333333333,
            12.0,
            7.833333333333333,
            15.0,
            33.333333333333336,
            72.0
        ],
        'clusters_y': [
            1.2,
            1.1666666666666665,
            4.333333333333333,
            4.3999999999999995,
            4.266666666666667,
            5.0
        ],
        'clusters_text': [
            ['b', 'B', 'ZZZ'],
            ['7', '7', '[unclear]7[/unclear]'],
            ['a', 'A', 'c'],
            ['page', 'page', 'page'],
            ['of', 'of', 'of'],
            ['text']
        ]
    },
    'frame1': {
        'clusters_x': [
            1.05,
            8.0
        ],
        'clusters_y': [
            0.9,
            1.0
        ],
        'clusters_text': [
            ['page', 'page', 'page'],
            ['2', '2', '2']
        ]
    }
}


class TestClusterLines(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_process_data(self):
        result = process_data(extracted_data)
        self.assertDictEqual(result, processed_data)

    def test_cluster_lines(self):
        result = poly_line_text_reducer._original(processed_data, eps=3, min_samples=1)
        self.assertDictEqual(result, reduced_data)

    def test_poly_line_text_reducer(self):
        result = poly_line_text_reducer(extracted_data, eps=3, min_samples=1)
        self.assertDictEqual(result, reduced_data)

    def test_poly_line_text_reducer_request(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }
        with app.test_request_context('/?eps=3&min_samples=1', **request_kwargs):
            result = poly_line_text_reducer(flask.request)
            self.assertDictEqual(result, reduced_data)


if __name__ == '__main__':
    unittest.main()
