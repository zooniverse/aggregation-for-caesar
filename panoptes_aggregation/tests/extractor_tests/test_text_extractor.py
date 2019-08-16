from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [{
        'task': 'T0',
        'value': 'test text'
    }]
}

expected = {
    'text': 'test text'
}

TestTextExtractor = ExtractorTest(
    extractors.text_extractor,
    classification,
    expected,
    'Test text extractor'
)
