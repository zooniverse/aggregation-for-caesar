from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

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

TestSWGraphic = ExtractorTest(
    extractors.sw_graphic_extractor,
    classification_sw,
    expected_sw,
    'Test SW graphic'
)

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

TestATGraphic = ExtractorTest(
    extractors.sw_graphic_extractor,
    classification_at,
    expected_at,
    'Test AT graphic'
)


classification_blank = {
    'annotations': []
}

expected_blank = {}

TestSWGraphicBlank = ExtractorTest(
    extractors.sw_graphic_extractor,
    classification_blank,
    expected_blank,
    'Test SW/AT graphic blank input'
)

classification_wrong = {
    'annotations': [
        {
            'value': 1,
            'task': 'T2'
        }
    ]
}

TestSWGraphicWrong = ExtractorTest(
    extractors.sw_graphic_extractor,
    classification_wrong,
    expected_blank,
    'Test SW/AT graphic wrong input'
)
