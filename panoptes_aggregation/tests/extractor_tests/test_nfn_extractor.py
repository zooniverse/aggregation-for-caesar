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
