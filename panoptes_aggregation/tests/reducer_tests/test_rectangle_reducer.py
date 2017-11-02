import unittest
import numpy as np
import flask
import json
from panoptes_aggregation.reducers.rectangle_reducer import process_data, rectangle_reducer
from panoptes_aggregation.reducers.test_utils import extract_in_data

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [8.0, 20.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [8.0, 20.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_width': [20.0],
            'T0_tool0_height': [20.0]
        }
    }
]

processed_data = {
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0),
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 8.0),
            (100.0, 0.0, 50.0, 20.0),
            (0.0, 100.0, 10.0, 8.0),
            (100.0, 0.0, 50.0, 20.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_rec_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rec_height': [20.0, 8.0, 20.0, 8.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [20.0, 8.0],
        'T0_tool1_rec_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rec_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rec_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rec_height': [8.0, 20.0, 8.0, 20.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [8.0, 20.0],
    },
    'frame1': {
        'T0_tool0_rec_x': [20.0],
        'T0_tool0_rec_y': [20.0],
        'T0_tool0_rec_width': [20.0],
        'T0_tool0_rec_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rec_x': [50.0, 50.0],
        'T0_tool1_rec_y': [50.0, 50.0],
        'T0_tool1_rec_width': [50.0, 50.0],
        'T0_tool1_rec_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
    }
}

extracted_data_sw = [
    {
        'frame0': {
            'tool0_x': [0.0, 100.0],
            'tool0_y': [0.0, 100.0],
            'tool0_width': [50.0, 10.0],
            'tool0_height': [20.0, 8.0],
            'tool0_tag': [
                '<graphic>seal</graphic>',
                '<graphic>seal</graphic>'
            ]
        }
    },
    {
        'frame0': {
            'tool0_x': [0.0, 100.0],
            'tool0_y': [0.0, 100.0],
            'tool0_width': [50.0, 10.0],
            'tool0_height': [20.0, 8.0],
            'tool0_tag': [
                '<graphic>seal</graphic>',
                '<graphic>text</graphic>'
            ]
        }
    }
]

processed_data_sw = {
    'frame0': {
        'tool0': [
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0),
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0)
        ],
        'tag': [
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>text</graphic>'
        ]
    }
}

reduced_data_sw = {
    'frame0': {
        'rec_tags': [
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>text</graphic>'
        ],
        'tool0_rec_x': [0.0, 100.0, 0.0, 100.0],
        'tool0_rec_y': [0.0, 100.0, 0.0, 100.0],
        'tool0_rec_width': [50.0, 10.0, 50.0, 10.0],
        'tool0_rec_height': [20.0, 8.0, 20.0, 8.0],
        'tool0_cluster_labels': [0, 1, 0, 1],
        'tool0_clusters_count': [2, 2],
        'tool0_clusters_x': [0.0, 100.0],
        'tool0_clusters_y': [0.0, 100.0],
        'tool0_clusters_width': [50.0, 10.0],
        'tool0_clusters_height': [20.0, 8.0],
    }
}


class TestRectangleReducer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_process_data(self):
        result = process_data(extracted_data)
        self.assertDictEqual(result, processed_data)

    def test_process_data_sw(self):
        result = process_data(extracted_data_sw)
        self.assertDictEqual(result, processed_data_sw)

    def test_reducer(self):
        result = rectangle_reducer(extracted_data, eps=5, min_samples=2)
        self.assertDictEqual(result, reduced_data)

    def test_reducer_sw(self):
        result = rectangle_reducer(extracted_data_sw, eps=5, min_samples=2)
        self.assertDictEqual(result, reduced_data_sw)

    def test_request(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data)),
            'content_type': 'application/json'
        }
        with app.test_request_context('/?eps=5&min_samples=2', **request_kwargs):
            result = rectangle_reducer(flask.request)
            self.assertDictEqual(result, reduced_data)

    def test_request_sw(self):
        app = flask.Flask(__name__)
        request_kwargs = {
            'data': json.dumps(extract_in_data(extracted_data_sw)),
            'content_type': 'application/json'
        }
        with app.test_request_context('/?eps=5&min_samples=2', **request_kwargs):
            result = rectangle_reducer(flask.request)
            self.assertDictEqual(result, reduced_data_sw)
