import unittest
from collections import Counter
import copy
import flask
import json
from panoptes_aggregation import reducers

extracted_data = [
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'grooming': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'interacting': 1.0, 'grooming': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'grooming': 1.0}, 'choice': 'blackbear'}
]

processed_data = {
    'blackbear': [
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'interacting': 1, 'grooming': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'grooming': 1})
        }
    ],
    'raccoon': [
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'grooming': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        }
    ]
}

reduced_data = [
    {
        'choice': 'raccoon',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers_howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers_whatistheanimalsdoing': {
            'standing': 3,
            'grooming': 1
        },
        'answers_clickwowifthisasanespeciallyawesomephoto': {
            'wow': 1
        }
    },
    {
        'choice': 'blackbear',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers_howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers_whatistheanimalsdoing': {
            'standing': 2,
            'grooming': 2,
            'interacting': 1
        },
        'answers_clickwowifthisasanespeciallyawesomephoto': {
            'wow': 2
        }
    }
]


class TestCountSurvey(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.extracted_data = copy.deepcopy(extracted_data)
        self.processed_data = copy.deepcopy(processed_data)
        self.reduced_data = copy.deepcopy(reduced_data)

    def test_process_data(self):
        result_data, result_count = reducers.survey_reducer.process_data(self.extracted_data)
        self.assertEqual(result_count, len(self.extracted_data))
        self.assertDictEqual(result_data, self.processed_data)

    def test_count_vote(self):
        result = reducers.survey_reducer.count_votes(self.processed_data, vote_count=len(self.extracted_data))
        self.assertCountEqual(result, self.reduced_data)

    def test_process_request(self):
        app = flask.Flask(__name__)
        extracted_request_data = []
        for data in self.extracted_data:
            extracted_request_data.append({'data': data})
        request_kwargs = {
            'data': json.dumps(copy.deepcopy(extracted_request_data)),
            'content_type': 'application/json'
        }
        with app.test_request_context(**request_kwargs):
            result = reducers.survey_reducer.survey_reducer_request(flask.request)
            self.assertCountEqual(result, self.reduced_data)


if __name__ == '__main__':
    unittest.main()
