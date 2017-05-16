import unittest
import json
import flask
import extractors


class TestPointExtractor(unittest.TestCase):
    def setUp(self):
        with open('tests/extractor_tests/kenisis_points.json', 'r') as f:
            self.kenisis_data = json.load(f)
        self.expected_result = {
            'T0_tool0_0_x': 452.18341064453125,
            'T0_tool0_0_y': 202.87478637695312,
            'T0_tool0_2_x': 190.54489135742188,
            'T0_tool0_2_y': 306.410888671875,
            'T0_tool0_6_x': 408.8101806640625,
            'T0_tool0_6_y': 235.054931640625,
            'T0_tool0_7_x': 411.60845947265625,
            'T0_tool0_7_y': 158.1024169921875,
            'T0_tool0_8_x': 482.96441650390625,
            'T0_tool0_8_y': 180.4886016845703,
            'T0_tool1_1_x': 404.61279296875,
            'T0_tool1_1_y': 583.4398803710938,
            'T0_tool1_3_x': 422.8015441894531,
            'T0_tool1_3_y': 568.0493774414062,
            'T0_tool1_4_x': 435.3937683105469,
            'T0_tool1_4_y': 612.82177734375,
            'T0_tool1_5_x': 371.03350830078125,
            'T0_tool1_5_y': 617.0191650390625
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
