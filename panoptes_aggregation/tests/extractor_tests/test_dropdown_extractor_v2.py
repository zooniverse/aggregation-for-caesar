from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'metadata': {
        'classifier_version': '2.0'
    },
    'annotations': [
        {
            'task': 'T0',
            'taskType': 'dropdown-simple',
            'value': {
                'selection': 6,
                'option': True
            }
        }
    ]
}

expected = {'value': [{'6': 1}]}

TestSimpleDropdown = ExtractorTest(
    extractors.dropdown_extractor,
    classification,
    expected,
    'Test simple-dropdown task for classifier v2.0',
    test_name='TestSimpleDropdown'
)
