import unittest
import json
import flask
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.test_utils import annotation_by_task

single_classification = {
    'annotations': [{
        "task": "T0",
        "task_label": "A single question",
        "value": "Yes"
    }]
}

multiple_classification = {
    'annotations': [{
        "task": "T1",
        "task_label": "A multi question",
        "value": ["Blue", "Green"]
    }]
}

single_expected = {'yes': 1}

multiple_expected = {'blue': 1, 'green': 1}


class TestQuestionExtractor(unittest.TestCase):
    def test_single(self):
        result = extractors.question_extractor(single_classification)
        self.assertDictEqual(result, single_expected)

    def test_single_request(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(single_classification)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.question_extractor(flask.request)
            self.assertDictEqual(result, single_expected)

    def test_multiple(self):
        result = extractors.question_extractor(multiple_classification)
        self.assertDictEqual(result, multiple_expected)

    def test_multiple_request(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(multiple_classification)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.question_extractor(flask.request)
            self.assertDictEqual(result, multiple_expected)


if __name__ == '__main__':
    unittest.main()
