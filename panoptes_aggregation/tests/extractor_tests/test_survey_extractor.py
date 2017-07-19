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
        self.expected = {
            'choice': ['agouti', 'peccarycollared', 'nothinghere'],
            'answers.HOWMANY': ['1', '3', 'null']
        }

    def test_extract(self):
        result = extractors.survey_extractor.classification_to_extract(self.classification)
        self.assertDictEqual(result, self.expected)

    def test_request(self):
        request_kwargs = {
            'data': json.dumps(self.classification),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            self.assertDictEqual(extractors.survey_extractor.survey_extractor_request(flask.request), self.expected)


if __name__ == '__main__':
    unittest.main()
