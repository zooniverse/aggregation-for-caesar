from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

single_classification = {
    'annotations': [{
        "task": "T0",
        "task_label": "A single question",
        "value": "Yes"
    }]
}

single_expected = {'yes': 1}

TestSingle = ExtractorTest(
    extractors.question_extractor,
    single_classification,
    single_expected,
    'Test single question'
)

multiple_classification = {
    'annotations': [{
        "task": "T1",
        "task_label": "A multi question",
        "value": ["Blue", "Green"]
    }]
}

multiple_expected = {'blue': 1, 'green': 1}

TestMultiple = ExtractorTest(
    extractors.question_extractor,
    multiple_classification,
    multiple_expected,
    'Test multiple question'
)

null_classification = {
    'annotations': [{
        "task": "T0",
        "task_label": "A single question",
        "value": None
    }]
}

null_expected = {'None': 1}

TestNull = ExtractorTest(
    extractors.question_extractor,
    null_classification,
    null_expected,
    'Test null question'
)
