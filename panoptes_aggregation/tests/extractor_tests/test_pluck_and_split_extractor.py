from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [],
    "subject": {"metadata": {"one": "alpha,beta,gamma", "two": "red,green,blue"}},
    "metadata": {"three": "a_b_c", "four": "1_2_3"},
}

expected_single = {"data": ["alpha", "beta", "gamma"]}
expected_split_str = {"data": ["a", "b", "c"]}
expected_multi = {"data": ["alpha", "beta", "blue", "gamma", "green", "red"]}

TestPluckAndSplitSingle = ExtractorTest(
    extractors.pluck_and_split_extractor,
    classification,
    expected_single,
    "Test pluck_and_split extractor with single matching field",
    kwargs={
        "path": "$.subject.metadata.one",
    },
    test_name="TestPluckAndSplitSingle",
)

TestPluckAndSplitStr = ExtractorTest(
    extractors.pluck_and_split_extractor,
    classification,
    expected_split_str,
    "Test pluck_and_split extractor with different split str",
    kwargs={
        "path": "$.metadata.three",
        "split_str": "_",
    },
    test_name="TestPluckAndSplitStr",
)

TestPluckAndSplitMulti = ExtractorTest(
    extractors.pluck_and_split_extractor,
    classification,
    expected_multi,
    "Test pluck_and_split extractor with multiple matches",
    kwargs={
        "path": "$.subject.metadata[*]",
    },
    test_name="TestPluckAndSplitMulti",
)
