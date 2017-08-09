import unittest
import json
import flask
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.test_utils import annotation_by_task

classification = {
    'annotations': [{
        'task': 'T0',
        'value': [
            {
                'choice': 'AGOUTI',
                'answers': {'HOWMANY': '1'},
                'filters': {}
            }, {
                'choice': 'PECCARYCOLLARED',
                'answers': {'HOWMANY': '3', 'WHATDOING': ['standing', 'sleeping']},
                'filters': {}
            }, {
                'choice': 'NOTHINGHERE',
                'answers': {},
                'filters': {}
            }
        ]
    }]
}

expected = [
    {
        'choice': 'agouti',
        'answers_howmany': {'1': 1}
    },
    {
        'choice': 'peccarycollared',
        'answers_howmany': {'3': 1},
        'answers_whatdoing': {'standing': 1, 'sleeping': 1}
    },
    {
        'choice': 'nothinghere',
    }
]


class TestSurveyExtractor(unittest.TestCase):
    def test_extract(self):
        result = extractors.survey_extractor(classification)
        for i in range(len(result)):
            with self.subTest(i=i):
                self.assertDictEqual(result[i], expected[i])

    def test_request(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.survey_extractor(flask.request)
            for i in range(len(result)):
                with self.subTest(i=i):
                    self.assertDictEqual(result[i], expected[i])


if __name__ == '__main__':
    unittest.main()
