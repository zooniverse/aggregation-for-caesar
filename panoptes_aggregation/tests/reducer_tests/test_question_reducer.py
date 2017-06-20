import unittest
from collections import Counter
import flask
import json
from panoptes_aggregation import reducers


class TestProcessData(unittest.TestCase):
    def setUp(self):
        self.extracted_data = [
            {'a': 1, 'b': 1},
            {'a': 1},
            {'b': 1, 'c': 1},
            {'b': 1, 'a': 1}
        ]

    def test_process_data(self):
        result = reducers.question_reducer.process_data(self.extracted_data)
        for r, e in zip(result, self.extracted_data):
            with self.subTest(i=e):
                # note: Counter is a sub-class of dict, so a DictEqual will work here
                self.assertDictEqual(r, e)

    def test_process_data_pairs(self):
        expected = [
            {'a+b': 1},
            {'a': 1},
            {'b+c': 1},
            {'a+b': 1}
        ]
        result = reducers.question_reducer.process_data(self.extracted_data, pairs=True)
        for r, e in zip(result, expected):
            with self.subTest(i=e):
                self.assertDictEqual(r, e)


class TestCountVote(unittest.TestCase):
    def setUp(self):
        self.processed_data = [
            Counter({'a': 1, 'b': 1}),
            Counter({'a': 1}),
            Counter({'b': 1, 'c': 1}),
            Counter({'b': 1, 'a': 1})
        ]
        self.expected = {'a': 3, 'b': 3, 'c': 1}
        self.processed_data_pairs = [
            Counter({'a+b': 1}),
            Counter({'a': 1}),
            Counter({'b+c': 1}),
            Counter({'a+b': 1})
        ]
        self.expected_pairs = {'a+b': 2, 'a': 1, 'b+c': 1}

    def test_count_vote(self):
        reuslt = reducers.question_reducer.count_votes(self.processed_data)
        self.assertDictEqual(reuslt, self.expected)

    def test_count_vote_pairs(self):
        reuslt = reducers.question_reducer.count_votes(self.processed_data_pairs)
        self.assertDictEqual(reuslt, self.expected_pairs)


class TestReducerRequest(unittest.TestCase):
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

    def test_process_request(self):
        expected = {'a': 3, 'b': 3, 'c': 1}
        with self.app.test_request_context(**self.request_kwargs):
            self.assertDictEqual(reducers.question_reducer.reducer_request(flask.request), expected)

    def test_process_request_pairs(self):
        expected = {'a+b': 2, 'a': 1, 'b+c': 1}
        with self.app.test_request_context('/?pairs=True', **self.request_kwargs):
            self.assertDictEqual(reducers.question_reducer.reducer_request(flask.request), expected)


if __name__ == '__main__':
    unittest.main()
