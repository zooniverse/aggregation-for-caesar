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

single_classification_two_tasks = {
    'annotations': [{
        "task": "T0",
        "task_label": "A single question 1",
        "value": "Yes"
    }, {
        "task": "T1",
        "task_label": "A single question 2",
        "value": "No"
    }]
}

single_expected_1 = {'yes': 1}
single_expected_2 = {'no': 1}

TestSingleTwoTasks = ExtractorTest(
    extractors.question_extractor,
    single_classification_two_tasks,
    single_expected_1,
    'Test multiple single questions passed in without task keyword'
)


TestSingleTwoTasks = ExtractorTest(
    extractors.question_extractor,
    single_classification_two_tasks,
    single_expected_2,
    'Test multiple single questions passed in with task keyword',
    kwargs={'task': 'T1'}
)
