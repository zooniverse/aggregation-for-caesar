from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [{
        'task': 'T0',
        'value': 3
    }]
}

expected = {'slider_value': 3}

TestSlider = ExtractorTest(
    extractors.slider_extractor,
    classification,
    expected,
    'Test slider'
)
