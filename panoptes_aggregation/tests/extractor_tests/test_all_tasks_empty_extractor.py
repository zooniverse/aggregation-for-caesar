from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

no_empty_classification = {
    "annotations": [
        {"task": "T0", "task_label": "A single question", "value": "Yes"},
        {"task": "T1", "task_label": "A multi question", "value": ["Blue", "Green"]},
        {
            "task": "T2",
            "value": [
                {
                    "frame": 0,
                    "tool": 0,
                    "y": 202.87478637695312,
                    "details": [],
                    "x": 452.18341064453125,
                },
                {
                    "frame": 0,
                    "tool": 1,
                    "y": 583.4398803710938,
                    "details": [],
                    "x": 404.61279296875,
                },
            ],
        },
    ]
}

no_empty_expected = {"result": False}

TestNoEmpty = ExtractorTest(
    extractors.all_tasks_empty_extractor,
    no_empty_classification,
    no_empty_expected,
    "Test for zero empty task values",
    test_name="TestNoEmpty",
    blank_extract={"result": True},
)

some_empty_classification = {
    "annotations": [
        {"task": "T0", "task_label": "A single question", "value": "Yes"},
        {"task": "T1", "task_label": "A multi question", "value": None},
        {
            "task": "T2",
            "value": [
                {
                    "frame": 0,
                    "tool": 0,
                    "y": 202.87478637695312,
                    "details": [],
                    "x": 452.18341064453125,
                },
                {
                    "frame": 0,
                    "tool": 1,
                    "y": 583.4398803710938,
                    "details": [],
                    "x": 404.61279296875,
                },
            ],
        },
    ]
}

some_empty_expected = {"result": False}

TestSomeEmpty = ExtractorTest(
    extractors.all_tasks_empty_extractor,
    some_empty_classification,
    some_empty_expected,
    "Test for some task values populated and some empty",
    test_name="TestSomeFull",
    blank_extract={"result": True},
)

all_empty_classification = {
    "annotations": [
        {"task": "T0", "task_label": "A single question", "value": None},
        {"task": "T1", "task_label": "A multi question", "value": None},
        {"task": "T2", "value": None},
    ]
}

all_empty_expected = {"result": True}

TestAllEmpty = ExtractorTest(
    extractors.all_tasks_empty_extractor,
    all_empty_classification,
    all_empty_expected,
    "Test for all task values empty",
    test_name="TestAllEmpty",
    blank_extract={"result": True},
)
