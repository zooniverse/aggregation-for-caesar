import unittest
from collections import Counter
import copy
import flask
import json
from panoptes_aggregation.reducers.survey_reducer import process_data, survey_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

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
        result_data, result_count = process_data(self.extracted_data)
        self.assertEqual(result_count, len(self.extracted_data))
        self.assertDictEqual(result_data, self.processed_data)

    def test_count_vote(self):
        result = survey_reducer._original((self.processed_data, len(self.extracted_data)))
        self.assertCountEqual(result, self.reduced_data)

    def test_survey_reducer(self):
        result = survey_reducer(self.extracted_data)
        self.assertCountEqual(result, self.reduced_data)

    def test_survey_reducer_request(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(self.extracted_data)),
            'content_type': 'application/json'
        }
        with app.test_request_context(**request_kwargs):
            result = survey_reducer(flask.request)
            self.assertCountEqual(result, self.reduced_data)


if __name__ == '__main__':
    unittest.main()
