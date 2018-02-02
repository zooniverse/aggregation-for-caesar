from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [
        {
            'task': 'T0',
            'value': [
                {
                    'value': 'Option 1',
                    'option': True
                },
                {
                    'value': 'Option 2',
                    'option': True
                },
                {
                    'value': None,
                    'option': False
                }
            ]
        }
    ]
}

expected = {
    'value': [
        {'option-1': 1},
        {'option-2': 1},
        {'None': 1}
    ]
}

TestDropdown = ExtractorTest(
    extractors.dropdown_extractor,
    classification,
    expected,
    'Test dropdown list'
)
