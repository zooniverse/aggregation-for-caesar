import unittest
import json
import flask
from panoptes_aggregation import extractors


class TestQuestionExtractor(unittest.TestCase):
    def setUp(self):
        self.single_classification = {
            'annotations': [{
                "task": "T0",
                "task_label": "A single question",
                "value": "Yes"
            }]
        }
        self.multiple_classification = {
            'annotations': [{
                "task": "T1",
                "task_label": "A multi question",
                "value": ["Blue", "Green"]
            }]
        }
        self.expected_single = {'yes': 1}
        self.expected_multiple = {'blue': 1, 'green': 1}

    def test_single(self):
        result = extractors.question_extractor.classification_to_extract(self.single_classification)
        self.assertDictEqual(result, self.expected_single)

    def test_single_request(self):
        request_kwargs = {
            'data': json.dumps(self.single_classification),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            self.assertDictEqual(extractors.question_extractor.question_extractor_request(flask.request), self.expected_single)

    def test_multiple(self):
        result = extractors.question_extractor.classification_to_extract(self.multiple_classification)
        self.assertDictEqual(result, self.expected_multiple)

    def test_multiple_request(self):
        request_kwargs = {
            'data': json.dumps(self.multiple_classification),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            self.assertDictEqual(extractors.question_extractor.question_extractor_request(flask.request), self.expected_multiple)


if __name__ == '__main__':
    unittest.main()
