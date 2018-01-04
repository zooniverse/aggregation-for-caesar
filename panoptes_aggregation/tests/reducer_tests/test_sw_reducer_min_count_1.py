import unittest
import urllib
import flask
import json
from panoptes_aggregation.reducers.poly_line_text_reducer import process_data, poly_line_text_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

extracted_data = [
    {
        'frame0': {
            'points': {
                'x': [
                    [860.71, 1418.89]
                ],
                'y': [
                    [267.38, 275.19]
                ]
            },
            'text': [
                ['Gather as many rose']
            ],
            'slope': [
                0.80162463698921349
            ]
        }
    }
]

processed_data = {
    'frame0': {
        'x': [
            [860.71, 1418.89]
        ],
        'y': [
            [267.38, 275.19]
        ],
        'text': [
            ['Gather as many rose']
        ],
        'slope': [
            0.80162463698921349
        ]
    }
}

reduced_data = {
    'frame0': [
        {
            'clusters_text': [
                ['Gather'],
                ['as'],
                ['many'],
                ['rose']
            ],
            'clusters_x': [860.71, 1418.89],
            'clusters_y': [267.38, 275.19],
            'consensus_score': 1.0,
            'gutter_label': 0,
            'line_slope': 0.80162463698921349,
            'number_views': 1,
            'slope_label': 0
        }
    ]
}


class TestSWClusterLinesMinSamples1(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.kwargs = {
            'eps_slope': 0.5,
            'eps_line': 15,
            'eps_word': 30,
            'dot_freq': 'line',
            'min_samples': 1
        }

    def test_process_data(self):
        result = process_data(extracted_data)
        self.assertDictEqual(dict(result), processed_data)

    def test_cluster_lines(self):
        result = poly_line_text_reducer._original(processed_data, metric='euclidean', gutter_tol=0, min_word_count=1, **self.kwargs)
        self.assertDictEqual(dict(result), reduced_data)

    def test_poly_line_text_reducer(self):
        result = poly_line_text_reducer(extracted_data, **self.kwargs)
        self.assertDictEqual(dict(result), reduced_data)

    def test_poly_line_text_reducer_request(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }
        url_params = '?{0}'.format(urllib.parse.urlencode(self.kwargs))
        with app.test_request_context(url_params, **request_kwargs):
            result = poly_line_text_reducer(flask.request)
            self.assertDictEqual(dict(result), reduced_data)


if __name__ == '__main__':
    unittest.main()
