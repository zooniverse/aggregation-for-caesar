import unittest
from collections import Counter
import copy
import flask
import json
from panoptes_aggregation import reducers

extracted_data = [
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.grooming': 1.0, 'choice': 'raccoon'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.standing': 1.0, 'choice': 'raccoon'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.standing': 1.0, 'answers.clickwowifthisasanespeciallyawesomephoto.wow': 1.0, 'choice': 'raccoon'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.standing': 1.0, 'choice': 'raccoon'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.interacting': 1.0, 'answers.whatistheanimalsdoing.grooming': 1.0, 'answers.clickwowifthisasanespeciallyawesomephoto.wow': 1.0, 'choice': 'blackbear'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.standing': 1.0, 'choice': 'blackbear'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.standing': 1.0, 'answers.clickwowifthisasanespeciallyawesomephoto.wow': 1.0, 'choice': 'blackbear'},
    {'answers.howmanyanimalsdoyousee.1': 1.0, 'answers.whatistheanimalsdoing.grooming': 1.0, 'choice': 'blackbear'}
]

processed_data = {
    'blackbear': [
        {
            'answers.clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'interacting': 1, 'grooming': 1})
        },
        {
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers.clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'grooming': 1})
        }
    ],
    'raccoon': [
        {
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'grooming': 1})
        },
        {
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers.clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers.howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers.whatistheanimalsdoing': Counter({'standing': 1})
        }
    ]
}

reduced_data = [
    {
        'choice': 'blackbear',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers.howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers.whatistheanimalsdoing': {
            'standing': 2,
            'grooming': 2,
            'interacting': 1
        },
        'answers.clickwowifthisasanespeciallyawesomephoto': {
            'wow': 2
        }
    },
    {
        'choice': 'raccoon',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers.howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers.whatistheanimalsdoing': {
            'standing': 3,
            'grooming': 1
        },
        'answers.clickwowifthisasanespeciallyawesomephoto': {
            'wow': 1
        }
    }
]


class TestProcessData(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.extracted_data = copy.deepcopy(extracted_data)
        self.expected = copy.deepcopy(processed_data)

    def test_process_data(self):
        result_data, result_count = reducers.survey_reducer.process_data(self.extracted_data)
        self.assertEqual(result_count, len(self.extracted_data))
        self.assertDictEqual(result_data, self.expected)


class TestCountVote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.processed_data = copy.deepcopy(processed_data)
        self.expected = copy.deepcopy(reduced_data)

    def test_count_vote(self):
        result = reducers.survey_reducer.count_votes(self.processed_data, vote_count=len(extracted_data))
        for rdx, r in enumerate(result):
            with self.subTest(i=rdx):
                self.assertDictEqual(dict(r), self.expected[rdx])


class TestReducerRequest(unittest.TestCase):
    def setUp(self):
        extracted_request_data = []
        for data in extracted_data:
            extracted_request_data.append({'data': data})
        self.app = flask.Flask(__name__)
        request_data = json.dumps(copy.deepcopy(extracted_request_data))
        self.request_kwargs = {
            'data': request_data,
            'content_type': 'application/json'
        }
        self.expected = copy.deepcopy(reduced_data)

    def test_process_request(self):
        with self.app.test_request_context(**self.request_kwargs):
            result = reducers.survey_reducer.survey_reducer_request(flask.request)
            for rdx, r in enumerate(result):
                with self.subTest(i=rdx):
                    self.assertDictEqual(dict(r), self.expected[rdx])


if __name__ == '__main__':
    unittest.main()
