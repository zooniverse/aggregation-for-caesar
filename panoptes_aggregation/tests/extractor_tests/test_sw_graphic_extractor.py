import unittest
import json
import flask
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.test_utils import annotation_by_task

classification_sw = {
    'annotations': [
        {
            'task': 'T2',
            'value': [
                {
                    'type': 'graphic',
                    'x': 0,
                    'y': 0,
                    'width': 5,
                    'height': 10,
                    'tag': '<graphic>seal</graphic>'
                },
                {
                    'type': 'graphic',
                    'x': 20,
                    'y': 25,
                    'width': 10,
                    'height': 5,
                    'tag': '<graphic>seal</graphic>'
                },
                {
                    'type': 'graphic',
                    'x': 100,
                    'y': 90,
                    'width': 24,
                    'height': 24,
                    'tag': '<graphic>seal</graphic>'
                }
            ]
        }
    ]
}

expected_sw = {
    'frame0': {
        'tool0_x': [0, 20, 100],
        'tool0_y': [0, 25, 90],
        'tool0_width': [5, 10, 24],
        'tool0_height': [10, 5, 24],
        'tool0_tag': [
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>'
        ]
    }
}

classification_at = {
    'annotations': [
        {
            'task': 'T2',
            'value': [
                {
                    'type': 'image',
                    'x': 0,
                    'y': 0,
                    'width': 5,
                    'height': 10
                },
                {
                    'type': 'image',
                    'x': 20,
                    'y': 25,
                    'width': 10,
                    'height': 5
                },
                {
                    'type': 'image',
                    'x': 100,
                    'y': 90,
                    'width': 24,
                    'height': 24
                }
            ]
        }
    ]
}

expected_at = {
    'frame0': {
        'tool0_x': [0, 20, 100],
        'tool0_y': [0, 25, 90],
        'tool0_width': [5, 10, 24],
        'tool0_height': [10, 5, 24]
    }
}


classification_blank = {
    'annotations': []
}

expected_blank = {}

classification_wrong = {
    'annotations': [
        {
            'value': 1,
            'task': 'T2'
        }
    ]
}


class TextSWGraphicExtractor(unittest.TestCase):
    def test_extract_sw(self):
        result = extractors.sw_graphic_extractor(classification_sw)
        self.assertDictEqual(result, expected_sw)

    def test_extract_at(self):
        result = extractors.sw_graphic_extractor(classification_at)
        self.assertDictEqual(result, expected_at)

    def test_request_sw(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification_sw)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.sw_graphic_extractor(flask.request)
            self.assertDictEqual(result, expected_sw)

    def test_request_at(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification_at)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.sw_graphic_extractor(flask.request)
            self.assertDictEqual(result, expected_at)

    def test_extract_blank(self):
        result = extractors.sw_graphic_extractor(classification_blank)
        self.assertDictEqual(result, expected_blank)

    def test_request_blank(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification_blank)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.sw_graphic_extractor(flask.request)
            self.assertDictEqual(result, expected_blank)

    def test_extract_wrong(self):
        result = extractors.sw_graphic_extractor(classification_wrong)
        self.assertDictEqual(result, expected_blank)

    def test_request_wrong(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification_wrong)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.sw_graphic_extractor(flask.request)
            self.assertDictEqual(result, expected_blank)
