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

expected = {"in_whitelist": 1, "not_in_whitelist": 1}


TestWhitelistCount = ExtractorTest(
    extractors.whitelist_count_extractor,
    classification,
    expected,
    "Test whitelist count",
    blank_extract={},
    test_name="TestWhitelistCount",
    kwargs={
        "path": "$.metadata.species_whitelist",
    },
)
