import unittest
import flask
import json
from panoptes_aggregation import reducers
from panoptes_aggregation.reducers.test_utils import extract_in_data

extracted_data = [
    {'variants': ['a', 'b']},
    {},
    {'variants': ['c']}
]

reduced_data = {
    'variants': [
        'a',
        'b',
        'c'
    ]
}


class TestSWVariantsReducer(unittest.TestCase):
    def test_reducer(self):
        result = reducers.sw_variant_reducer(extracted_data)
        self.assertDictEqual(result, reduced_data)

    def test_request(self):
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = reducers.sw_variant_reducer(flask.request)
            self.assertDictEqual(result, reduced_data)
