from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [{
        'task': 'T0',
        'value': [
            {
                'choice': 'AGOUTI',
                'answers': {'HOWMANY': '1'},
                'filters': {}
            }, {
                'choice': 'PECCARYCOLLARED',
                'answers': {'HOWMANY': '3', 'WHATDOING': ['standing', 'sleeping']},
                'filters': {}
            }, {
                'choice': 'NOTHINGHERE',
                'answers': {},
                'filters': {}
            }
        ]
    }]
}

expected = [
    {
        'choice': 'agouti',
        'answers_howmany': {'1': 1}
    },
    {
        'choice': 'peccarycollared',
        'answers_howmany': {'3': 1},
        'answers_whatdoing': {'standing': 1, 'sleeping': 1}
    },
    {
        'choice': 'nothinghere',
    }
]


TestSurvey = ExtractorTest(
    extractors.survey_extractor,
    classification,
    expected,
    'Test survey',
    blank_extract=[],
    test_type='assertCountEqual'
)
