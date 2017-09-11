import unittest
import json
import flask
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.test_utils import annotation_by_task

classification = {
    "annotations": [
        {
            "task": "T0",
            "task_label": "Add a point directly below the centre of every word that you can transcribe.",
            "value": [
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 756.9894409179688, "y": 197.12567138671875}
                    ],
                    "details": [
                        {"value": "[unclear]Cipher[/unclear]"}
                    ],
                    "tool_label": "Transcribed word marker"
                },
                {
                    "tool": 0,
                    "frame": 0,
                    "closed": True,
                    "points": [
                        {"x": 565.92919921875, "y": 324.4991760253906},
                        {"x": 872.2321166992188, "y": 321.46649169921875},
                        {"x": 1020.8345947265625, "y": 318.43377685546875},
                        {"x": 1151.2408447265625, "y": 318.43377685546875}
                    ],
                    "details": [
                        {"value": "Recd Feb 2 1862"}
                    ],
                    "tool_label": "Transcribed word marker"
                },
                {
                    "tool": 0,
                    "frame": 1,
                    "closed": True,
                    "points": [
                        {"x": 402.1632385253906, "y": 488.26513671875},
                        {"x": 587.1580810546875, "y": 488.26513671875},
                        {"x": 832.8070068359375, "y": 488.26513671875},
                        {"x": 1045.09619140625, "y": 482.1997375488281}
                    ],
                    "details": [
                        {"value": "to July 30th 1862"}
                    ],
                    "tool_label": "Transcribed word marker"}
            ]
        }
    ]
}

expected = {
    'frame0': {
        'points': {
            'x':
                [
                    [
                        756.9894409179688
                    ],
                    [
                        565.92919921875,
                        872.2321166992188,
                        1020.8345947265625,
                        1151.2408447265625
                    ]
                ],
            'y':
                [
                    [
                        197.12567138671875
                    ],
                    [
                        324.4991760253906,
                        321.46649169921875,
                        318.43377685546875,
                        318.43377685546875
                    ]
                ]
        },
        'text': [
            [
                "[unclear]Cipher[/unclear]"
            ],
            [
                "Recd",
                "Feb",
                "2",
                "1862"
            ]
        ],
        'slope': [
            0,
            -0.6431845183798341
        ]
    },
    'frame1': {
        'points': {
            'x':
                [
                    [
                        402.1632385253906,
                        587.1580810546875,
                        832.8070068359375,
                        1045.09619140625
                    ]
                ],
            'y':
                [
                    [
                        488.26513671875,
                        488.26513671875,
                        488.26513671875,
                        482.1997375488281
                    ]
                ]
        },
        'text': [
            [
                "to",
                "July",
                "30th",
                "1862"
            ]
        ],
        'slope': [
            -0.48129253221574736
        ]
    }
}


class TestPolyLineTextExtractor(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_extract(self):
        result = extractors.poly_line_text_extractor(classification)
        self.assertDictEqual(result, expected)

    def test_request(self):
        request_kwargs = {
            'data': json.dumps(annotation_by_task(classification)),
            'content_type': 'application/json'
        }
        app = flask.Flask(__name__)
        with app.test_request_context(**request_kwargs):
            result = extractors.poly_line_text_extractor(flask.request)
            self.assertDictEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
