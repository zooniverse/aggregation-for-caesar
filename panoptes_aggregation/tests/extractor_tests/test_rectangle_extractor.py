import unittest
import json
import flask
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.test_utils import annotation_by_task

classification = {
    'annotations': [
        {
            'task': 'T2',
            'value': [
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 0,
                    'y': 0,
                    'width': 5,
                    'height': 10,
                },
                {
                    'tool': 0,
                    'frame': 0,
                    'x': 20,
                    'y': 25,
                    'width': 10,
                    'height': 5,
                },
                {
                    'tool': 1,
                    'frame': 0,
                    'x': 100,
                    'y': 90,
                    'width': 24,
                    'height': 24,
                },
                {
                    'tool': 0,
                    'frame': 1,
                    'x': 110,
                    'y': 91,
                    'width': 27,
                    'height': 50,
                }
            ]
        }
    ]
}

expected = {
    'frame0': {
        'T2_tool0_x': [0, 20],
        'T2_tool0_y': [0, 25],
        'T2_tool0_width': [5, 10],
        'T2_tool0_height': [10, 5],
        'T2_tool1_x': [100],
        'T2_tool1_y': [90],
        'T2_tool1_width': [24],
        'T2_tool1_height': [24],
    },
    'frame1': {
        'T2_tool0_x': [110],
        'T2_tool0_y': [91],
        'T2_tool0_width': [27],
        'T2_tool0_height': [50],
    }
}


class TextSWGraphicExtractor(unittest.TestCase):
    def test_extract(self):
        result = extractors.rectangle_extractor(classification)
        self.assertDictEqual(result, expected)

    def test_request_sw(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.rectangle_extractor(flask.request)
            self.assertDictEqual(result, expected)
