import unittest
from collections import Counter
import flask
import json
from panoptes_aggregation import reducers

extracted_data = [
    {'a': 1, 'b': 1},
    {'a': 1},
    {'b': 1, 'c': 1},
    {'b': 1, 'a': 1}
]

processed_data = [
    Counter({'a': 1, 'b': 1}),
    Counter({'a': 1}),
    Counter({'b': 1, 'c': 1}),
    Counter({'b': 1, 'a': 1})
]

processed_data_pairs = [
    Counter({'a+b': 1}),
    Counter({'a': 1}),
    Counter({'b+c': 1}),
    Counter({'a+b': 1})
]

reduced_data = {
    'a': 3,
    'b': 3,
    'c': 1
}

reduced_data_pairs = {
    'a+b': 2,
    'a': 1,
    'b+c': 1
}


class TestCountQuestions(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        request_data = json.dumps([
            {'data': {'a': 1, 'b': 1}},
            {'data': {'a': 1}},
            {'data': {'b': 1, 'c': 1}},
            {'data': {'b': 1, 'a': 1}}
        ])
        self.request_kwargs = {
            'data': request_data,
            'content_type': 'application/json'
        }

    def test_process_data(self):
        result = reducers.question_reducer.process_data(extracted_data)
        self.assertCountEqual(result, processed_data)

    def test_process_data_pairs(self):
        result = reducers.question_reducer.process_data(extracted_data, pairs=True)
        self.assertCountEqual(result, processed_data_pairs)

    def test_count_vote(self):
        reuslt = reducers.question_reducer.count_votes(processed_data)
        self.assertDictEqual(reuslt, reduced_data)

    def test_count_vote_pairs(self):
        reuslt = reducers.question_reducer.count_votes(processed_data_pairs)
        self.assertDictEqual(reuslt, reduced_data_pairs)

    def test_process_request(self):
        with self.app.test_request_context(**self.request_kwargs):
            result = reducers.question_reducer.question_reducer_request(flask.request)
            self.assertDictEqual(result, reduced_data)

    def test_process_request_pairs(self):
        with self.app.test_request_context('/?pairs=True', **self.request_kwargs):
            result = reducers.question_reducer.question_reducer_request(flask.request)
            self.assertDictEqual(result, reduced_data_pairs)


if __name__ == '__main__':
    unittest.main()
