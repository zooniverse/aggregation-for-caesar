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
    'Test single question',
    test_name='TestSingle'
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
    'Test multiple question',
    test_name='TestMultiple'
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
    'Test null question',
    test_name='TestNull'
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

TestSingleTwoTasksNoKey = ExtractorTest(
    extractors.question_extractor,
    single_classification_two_tasks,
    single_expected_1,
    'Test multiple single questions passed in without task keyword',
    test_name='TestSingleTwoTasksNoKey'
)


TestSingleTwoTasksKey = ExtractorTest(
    extractors.question_extractor,
    single_classification_two_tasks,
    single_expected_2,
    'Test multiple single questions passed in with task keyword',
    kwargs={'task': 'T1'},
    test_name='TestSingleTwoTasksKey'
)

single_pluck_classification = {
    "id": 359841171,
    "annotations": [{
        "task": "T0",
        "value": "0"
    }],
    "subject": {
        "id": 68561182,
        "metadata": {
            "filename": "uds_H.gf19767.png",
            "uber_flag_digit": "4",
            "is_gold_standard": "False"
        }
    }
}

single_pluck_keys = {
    "gold_standard": "subject.metadata.is_gold_standard",
    "true_value": "subject.metadata.uber_flag_digit"
}

single_pluck_expected = {
    "0": 1,
    "pluck.gold_standard": "False",
    "pluck.true_value": "4"
}

TestSinglePluck = ExtractorTest(extractors.question_extractor,
    single_pluck_classification,
    single_pluck_expected,
    "Test pluck field functionality with a question extractor",
    kwargs={'pluck': single_pluck_keys},
    test_name='TestSinglePluck')


feedback_pluck_classification = {
    "id": 359841171,
    "annotations": [{
        "task": "T0",
        "value": "0",
        "taskType": "single"
    }],
    "metadata": {
        "feedback": {
            "T0": [
                {
                    "answer": "0",
                    "success": True,
                    "strategy": "singleAnswerQuestion"
                }
            ]
        }
    },
    "subject": {
        "id": 68561182,
        "metadata": {
            "filename": "uds_H.gf19767.png",
        }
    }
}

feedback_pluck_keys = {
    "feedback": "metadata.feedback.T0"
}

feedback_pluck_expected = {
    "0": 1,
    "feedback": {
        "agreement_score": 1.0,
        "success": [
            True
        ],
        "true_answer": [
            "0"
        ]
    }
}

TestFeedbackPluck = ExtractorTest(
    extractors.question_extractor,
    feedback_pluck_classification,
    feedback_pluck_expected,
    "Test pluck field functionality for feedback data with a question extractor",
    kwargs={'pluck': feedback_pluck_keys},
    test_name='TestFeedbackPluck'
)

feedback_empty_pluck_classification = {
    "id": 359841171,
    "annotations": [{
        "task": "T0",
        "value": "0",
        "taskType": "single"
    }],
    "metadata": {
        "feedback": {}
    },
    "subject": {
        "id": 68561182,
        "metadata": {
            "filename": "uds_H.gf19767.png",
        }
    }
}

feedback_empty_pluck_keys = {
    "feedback": "metadata.feedback.T0"
}

feedback_empty_pluck_expected = {
    "0": 1,
}

TestFeedbackEmptyPluck = ExtractorTest(
    extractors.question_extractor,
    feedback_empty_pluck_classification,
    feedback_empty_pluck_expected,
    "Test pluck field functionality for question extractor with empty feedback fields",
    kwargs={'pluck': feedback_empty_pluck_keys},
    test_name='TestFeedbackEmptyPluck'
)
