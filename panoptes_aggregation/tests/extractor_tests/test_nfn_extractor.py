from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [
        {
            "task": "T10",
            "value": [
                {
                    "value": 1982,
                    "option": True
                }
            ]
        },
        {
            "task": "T1",
            "value": [
                {
                    "value": "United States",
                    "option": True
                }
            ]
        },
        {
            "task": "T3",
            "value": 5
        }
    ],
    "subject": {
        "metadata": {}
    },
    "metadata": {
        "utc_offset": "21600",
    },
    "created_at": "2019-01-14T19:28:13.667Z",
}

expected = {
    "workflow": "herbarium",
    "decade": "80s",
    "time": "nightowl",
    "country": "United States"
}

TestNfN = ExtractorTest(
    extractors.nfn_extractor,
    classification,
    expected,
    'Test NfN with year and country tasks specified done at night',
    kwargs={'year': 'T10', 'workflow': 'herbarium', 'country': "T1"}
)

classification_0 = {
    "annotations": [{
        "task": "T99",
        "value": [
            {
                "task": "T11",
                "value": [
                    {
                        "value": 2001,
                        "option": True
                    }
                ]
            }
        ]
    }],
    "metadata": {
        "utc_offset": "21600",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2019-04-22T06:28:13.667Z",
}

expected_0 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "earth_day": True,
    "country": "United States"
}

TestNfNTwo = ExtractorTest(
    extractors.nfn_extractor,
    classification_0,
    expected_0,
    'Test NfN on Earth Day with year as nested task and country from metadata. At lunchtime, local time.',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'}
)

classification_1 = {
    "annotations": [
        {
            "task": "T10",
            "value": 1976
        }
    ],
    "metadata": {
        "utc_offset": "21600",
    },
    "subject": {
        "metadata": {}
    },
    "created_at": "2019-05-22T06:28:13.667Z",
}

expected_1 = {
    "workflow": "herbarium",
    "decade": "70s",
    "time": "lunchbreak"
}

TestNfNThree = ExtractorTest(
    extractors.nfn_extractor,
    classification_1,
    expected_1,
    'Test NfN bare integer year annotation at lunchtime.',
    kwargs={'year': 'T10', 'workflow': 'herbarium'}
)

classification_bad_year = {
    "annotations": [
        {
            "task": "T10",
            "value": "n"
        }
    ],
    "metadata": {
        "utc_offset": "21600",
    },
    "subject": {
        "metadata": {}
    },
    "created_at": "2019-05-22T06:28:13.667Z",
}

expected_no_year = {
    "workflow": "herbarium",
    "time": "lunchbreak"
}

TestNfNBadYear = ExtractorTest(
    extractors.nfn_extractor,
    classification_bad_year,
    expected_no_year,
    'Test NfN bare integer year annotation at lunchtime with porly formatted year',
    kwargs={'year': 'T10', 'workflow': 'herbarium'}
)

TestNfNNoYear = ExtractorTest(
    extractors.nfn_extractor,
    classification_1,
    expected_no_year,
    'Test NfN bare integer year annotation at lunchtime with no year keyword',
    kwargs={'workflow': 'herbarium'}
)

classification_earlybird = {
    "annotations": [
        {
            "task": "T10",
            "value": 1976
        }
    ],
    "metadata": {
        "utc_offset": "21600",
    },
    "subject": {
        "metadata": {}
    },
    "created_at": "2019-05-22T22:28:13.667Z",
}

expected_earlybird = {
    "workflow": "herbarium",
    "decade": "70s",
    "time": "earlybird"
}

TestNfNEarlybird = ExtractorTest(
    extractors.nfn_extractor,
    classification_earlybird,
    expected_earlybird,
    'Test NfN bare integer year annotation at earlybird ',
    kwargs={'year': 'T10', 'workflow': 'herbarium'}
)

classification_dinnertime = {
    "annotations": [
        {
            "task": "T10",
            "value": 1976
        }
    ],
    "metadata": {
        "utc_offset": "21600",
    },
    "subject": {
        "metadata": {}
    },
    "created_at": "2019-05-22T10:28:13.667Z",
}

expected_dinnertime = {
    "workflow": "herbarium",
    "decade": "70s",
    "time": "dinnertime"
}

TestNfNDinnertime = ExtractorTest(
    extractors.nfn_extractor,
    classification_dinnertime,
    expected_dinnertime,
    'Test NfN bare integer year annotation at dinnertime',
    kwargs={'year': 'T10', 'workflow': 'herbarium'}
)

TestNfNNotInMetadataOrParams = ExtractorTest(
    extractors.nfn_extractor,
    classification_dinnertime,
    expected_dinnertime,
    'Test NfN bare integer year annotation at dinnertime with no state info in metadata',
    kwargs={'year': 'T10', 'workflow': 'herbarium', 'state': 'metadata'}
)
