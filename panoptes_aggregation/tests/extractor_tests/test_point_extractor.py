import unittest
import json
import flask
from panoptes_aggregation import extractors


class TestPointExtractor(unittest.TestCase):
    def setUp(self):
        with open('panoptes_aggregation/tests/extractor_tests/kenisis_points.json', 'r') as f:
            self.kenisis_data = json.load(f)
        self.expected_result = {
            'T0_tool0_x': [
                452.18341064453125,
                190.54489135742188,
                408.8101806640625,
                411.60845947265625,
                482.96441650390625
            ],
            'T0_tool0_y': [
                202.87478637695312,
                306.410888671875,
                235.054931640625,
                158.1024169921875,
                180.4886016845703
            ],
            'T0_tool1_x': [
                404.61279296875,
                422.8015441894531,
                435.3937683105469,
                371.03350830078125
            ],
            'T0_tool1_y': [
                583.4398803710938,
                568.0493774414062,
                612.82177734375,
                617.0191650390625
            ]
        }

    def test_extract(self):
        result = extractors.point_extractor.classification_to_extract(self.kenisis_data)
        self.assertDictEqual(result, self.expected_result)

    def test_extract_request(self):
        request_kwargs = {
            'data': json.dumps(self.kenisis_data),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            self.assertDictEqual(extractors.point_extractor.extractor_request(flask.request), self.expected_result)


if __name__ == '__main__':
    unittest.main()
