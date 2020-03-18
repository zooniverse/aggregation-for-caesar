from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {

    'annotations': [{
        'task': 'T0',
        'value': 'test text'
    }]
}

expected = {
    'text': 'test text',
    'gold_standard': False
}

TestTextExtractor = ExtractorTest(
    extractors.text_extractor,
    classification,
    expected,
    'Test text extractor',
    test_name='TestTextExtractor'
)

gold_classification = {
    'gold_standard': True,
    'annotations': [{
        'task': 'T0',
        'value': 'test text'
    }]
}

gold_expected = {
    'text': 'test text',
    'gold_standard': True
}

TestTextExtractorGold = ExtractorTest(
    extractors.text_extractor,
    classification,
    expected,
    'Test text extractor that is gold standard',
    test_name='TestTextExtractorGold'
)
