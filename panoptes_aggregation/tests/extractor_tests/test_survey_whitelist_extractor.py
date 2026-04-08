from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [
        {
            "task": "T0",
            "value": [
                {"choice": "AGOUTI", "answers": {"HOWMANY": "1"}, "filters": {}},
                {
                    "choice": "PECCARYCOLLARED",
                    "answers": {"HOWMANY": "3", "WHATDOING": ["standing", "sleeping"]},
                    "filters": {},
                },
                {"choice": "NOTHINGHERE", "answers": {}, "filters": {}},
            ],
        }
    ],
    "metadata": {"species_whitelist": "AGOUTI, PECCARYCOLLARED"},
}

expected = [
    {"choice": "agouti", "answers_howmany": {"1": 1}, "in_whitelist": True},
    {
        "choice": "peccarycollared",
        "answers_howmany": {"3": 1},
        "answers_whatdoing": {"standing": 1, "sleeping": 1},
        "in_whitelist": True,
    },
    {"choice": "nothinghere", "in_whitelist": False},
]


TestSurveyWhitelist = ExtractorTest(
    extractors.survey_whitelist_extractor,
    classification,
    expected,
    "Test survey whitelist",
    blank_extract=[],
    test_type="assertCountEqual",
    test_name="TestSurveyWhitelist",
    kwargs={
        "path": "$.metadata.species_whitelist",
    },
)
