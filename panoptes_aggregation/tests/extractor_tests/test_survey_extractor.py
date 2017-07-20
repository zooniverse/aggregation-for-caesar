import unittest
import json
import flask
from panoptes_aggregation import extractors


class TestSurveyExtractor(unittest.TestCase):
    def setUp(self):
        self.classification = {
            'annotations': [{
                'task': 'T0',
                'value': [
                    {
                        'choice': 'AGOUTI',
                        'answers': {'HOWMANY': '1'},
                        'filters': {}
                    }, {
                        'choice': 'PECCARYCOLLARED',
                        'answers': {'HOWMANY': '3'},
                        'filters': {}
                    }, {
                        'choice': 'NOTHINGHERE',
                        'answers': {},
                        'filters': {}
                    }
                ]
            }]
        }
        self.expected = [
            {
                'choice': 'agouti',
                'answers.howmany': '1'
            },
            {
                'choice': 'peccarycollared',
                'answers.howmany': '3'
            },
            {
                'choice': 'nothinghere',
            }
        ]

    def test_extract(self):
        result = extractors.survey_extractor.classification_to_extract(self.classification)
        for i in range(len(result)):
            with self.subTest(i=i):
                self.assertDictEqual(result[i], self.expected[i])

    def test_request(self):
        request_kwargs = {
            'data': json.dumps(self.classification),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.survey_extractor.survey_extractor_request(flask.request)
            for i in range(len(result)):
                with self.subTest(i=i):
                    self.assertDictEqual(result[i], self.expected[i])


if __name__ == '__main__':
    unittest.main()
