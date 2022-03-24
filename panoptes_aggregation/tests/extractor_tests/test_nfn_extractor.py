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
    kwargs={'year': 'T10', 'workflow': 'herbarium', 'country': "T1"},
    test_name='TestNfN'
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
    'Test NfN on Earth Day with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNTwo'
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
    'Test NfN bare integer year annotation at lunchtime',
    kwargs={'year': 'T10', 'workflow': 'herbarium'},
    test_name='TestNfNThree'
)

classification_we_dig_bio_october_2020 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2020-10-16T05:30:00.000Z",
}

expected_we_dig_bio_october_2020 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "we_dig_bio": 2020,
    "country": "United States"
}

TestNfNWeDigBioOctober2020 = ExtractorTest(
    extractors.nfn_extractor,
    classification_we_dig_bio_october_2020,
    expected_we_dig_bio_october_2020,
    'Test NfN during October, 2020, WeDigBio event with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNWeDigBioOctober2020'
)

classification_not_we_dig_bio_2020 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2020-07-16T05:30:00.000Z",
}

expected_not_we_dig_bio_2020 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "country": "United States"
}

TestNfNNotWeDigBio2020 = ExtractorTest(
    extractors.nfn_extractor,
    classification_not_we_dig_bio_2020,
    expected_not_we_dig_bio_2020,
    'Test NfN during 2020, not during a WeDigBio event, with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNNotWeDigBio2020'
)

classification_we_dig_bio_april_2021 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2021-04-09T05:30:00.000Z",
}

expected_we_dig_bio_april_2021 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "we_dig_bio": 2021,
    "country": "United States"
}

TestNfNWeDigBioApril2021 = ExtractorTest(
    extractors.nfn_extractor,
    classification_we_dig_bio_april_2021,
    expected_we_dig_bio_april_2021,
    'Test NfN during April, 2021, WeDigBio event with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNWeDigBioApril2021'
)

classification_we_dig_bio_october_2021 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2021-10-15T05:30:00.000Z",
}

expected_we_dig_bio_october_2021 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "we_dig_bio": 2021,
    "country": "United States"
}

TestNfNWeDigBioOctober2021 = ExtractorTest(
    extractors.nfn_extractor,
    classification_we_dig_bio_october_2021,
    expected_we_dig_bio_october_2021,
    'Test NfN during October, 2021, WeDigBio event with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNWeDigBioOctober2021'
)

classification_not_we_dig_bio_2021 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2021-07-16T05:30:00.000Z",
}

expected_not_we_dig_bio_2021 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "country": "United States"
}

TestNfNNotWeDigBio2021 = ExtractorTest(
    extractors.nfn_extractor,
    classification_not_we_dig_bio_2021,
    expected_not_we_dig_bio_2021,
    'Test NfN during 2021, not during a WeDigBio event, with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNNotWeDigBio2021'
)

classification_we_dig_bio_april_2022 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2022-04-09T05:30:00.000Z",
}

expected_we_dig_bio_april_2022 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "we_dig_bio": 2022,
    "country": "United States"
}

TestNfNWeDigBioApril2022 = ExtractorTest(
    extractors.nfn_extractor,
    classification_we_dig_bio_april_2022,
    expected_we_dig_bio_april_2022,
    'Test NfN during April, 2022, WeDigBio event with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNWeDigBioApril2022'
)

classification_we_dig_bio_october_2022 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2022-10-14T05:30:00.000Z",
}

expected_we_dig_bio_october_2022 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "we_dig_bio": 2022,
    "country": "United States"
}

TestNfNWeDigBioOctober2022 = ExtractorTest(
    extractors.nfn_extractor,
    classification_we_dig_bio_october_2022,
    expected_we_dig_bio_october_2022,
    'Test NfN during October, 2022, WeDigBio event with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNWeDigBioOctober2022'
)

classification_not_we_dig_bio_2022 = {
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
        "utc_offset": "18000",
    },
    "subject": {
        "metadata": {
            "country": "United States",
        }
    },
    "created_at": "2022-07-16T05:30:00.000Z",
}

expected_not_we_dig_bio_2022 = {
    "workflow": "herbarium",
    "decade": "00s",
    "time": "lunchbreak",
    "country": "United States"
}

TestNfNNotWeDigBio2022 = ExtractorTest(
    extractors.nfn_extractor,
    classification_not_we_dig_bio_2022,
    expected_not_we_dig_bio_2022,
    'Test NfN during 2022, not during a WeDigBio event, with year as nested task and country from metadata at lunchtime local time',
    kwargs={'year': 'T11', 'workflow': 'herbarium', 'country': 'metadata'},
    test_name='TestNfNNotWeDigBio2022'
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
    'Test NfN bare integer year annotation at lunchtime with poorly formatted year',
    kwargs={'year': 'T10', 'workflow': 'herbarium'},
    test_name='TestNfNBadYear'
)

TestNfNNoYear = ExtractorTest(
    extractors.nfn_extractor,
    classification_1,
    expected_no_year,
    'Test NfN bare integer year annotation at lunchtime with no year keyword',
    kwargs={'workflow': 'herbarium'},
    test_name='TestNfNNoYear'
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
    kwargs={'year': 'T10', 'workflow': 'herbarium'},
    test_name='TestNfNEarlybird'
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
    kwargs={'year': 'T10', 'workflow': 'herbarium'},
    test_name='TestNfNDinnertime'
)

TestNfNNotInMetadataOrParams = ExtractorTest(
    extractors.nfn_extractor,
    classification_dinnertime,
    expected_dinnertime,
    'Test NfN bare integer year annotation at dinnertime with no state info in metadata',
    kwargs={'year': 'T10', 'workflow': 'herbarium', 'state': 'metadata'},
    test_name='TestNfNNotInMetadataOrParams'
)

classification_multiselect = {
    "annotations": [
        {
            "task": "T1",
            "value": [4]
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

expected_multiselect = {
    "workflow": "labs",
    "time": "dinnertime"
}

TestNfNMultiselect = ExtractorTest(
    extractors.nfn_extractor,
    classification_multiselect,
    expected_multiselect,
    'Test NfN multiselect (array of ints) in a single task',
    kwargs={'workflow': 'labs'},
    test_name='TestNfNMultiselect'
)
