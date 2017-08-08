import unittest
from collections import Counter
import flask
import json
from panoptes_aggregation.reducers.question_reducer import process_data, question_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

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
        self.request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }

    def test_process_data(self):
        result = process_data(extracted_data)
        self.assertCountEqual(result, processed_data)

    def test_process_data_pairs(self):
        result = process_data(extracted_data, pairs=True)
        self.assertCountEqual(result, processed_data_pairs)

    def test_count_vote(self):
        reuslt = question_reducer._original(processed_data)
        self.assertDictEqual(reuslt, reduced_data)

    def test_count_vote_pairs(self):
        reuslt = question_reducer._original(processed_data_pairs)
        self.assertDictEqual(reuslt, reduced_data_pairs)

    def test_question_reducer(self):
        reuslt = question_reducer(extracted_data)
        self.assertDictEqual(reuslt, reduced_data)

    def test_question_reducer_pairs(self):
        reuslt = question_reducer(extracted_data, pairs=True)
        self.assertDictEqual(reuslt, reduced_data_pairs)

    def test_question_reducer_request(self):
        with self.app.test_request_context(**self.request_kwargs):
            result = question_reducer(flask.request)
            self.assertDictEqual(result, reduced_data)

    def test_question_reducer_request_pairs(self):
        with self.app.test_request_context('/?pairs=True', **self.request_kwargs):
            result = question_reducer(flask.request)
            self.assertDictEqual(result, reduced_data_pairs)


if __name__ == '__main__':
    unittest.main()
