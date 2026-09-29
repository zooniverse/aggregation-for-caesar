import unittest
from panoptes_aggregation.details_convert import (
    details_flatten,
    details_unflatten,
    details_extract_flatten
)


flat_example = {
    'T0_toolIndex0_subtask1': 'dropdown_extractor',
    'T0_toolIndex0_subtask0': 'question_extractor',
    'T0_toolIndex0_subtask2': None,
    'T0_toolIndex1_subtask0': 'question_extractor',
    'T0_toolIndex1_subtask1': 'dropdown_extractor'
}

unflat_example = {
    'T0_tool0': [
        'question_extractor',
        'dropdown_extractor',
        None
    ],
    'T0_tool1': [
        'question_extractor',
        'dropdown_extractor'
    ]
}

extract_details_v1 = {
    "other_keys": True,
    "T0_tool0_details": [
        [{"1": 1}, {"2": 1}],
        [{"3": 1}, {"4": 1}]
    ]
}


extract_details_v2 = {
    "other_keys": True,
    "T0_toolIndex0_subtask0": [{"1": 1}, {"3": 1}],
    "T0_toolIndex0_subtask1": [{"2": 1}, {"4": 1}],
}


class TestDetailsConvert(unittest.TestCase):
    def test_flatten(self):
        '''Test v1.0 to v2.0 details config conversion'''
        result = details_flatten(unflat_example)
        self.assertDictEqual(result, flat_example)

    def test_flatten_no_op(self):
        '''Test v2.0 to v2.0 details config conversion'''
        result = details_flatten(flat_example)
        self.assertDictEqual(result, flat_example)

    def test_unflatten(self):
        '''Test v2.0 to v1.0 details config conversion'''
        result = details_unflatten(flat_example)
        self.assertDictEqual(result, unflat_example)

    def test_unflatten_no_op(self):
        '''Test v1.0 to v1.0 details config conversion'''
        result = details_unflatten(unflat_example)
        self.assertDictEqual(result, unflat_example)

    def test_flatten_extract(self):
        '''Test v1.0 to v2.0 extract details conversion'''
        result = details_extract_flatten(extract_details_v1)
        self.assertDictEqual(result, extract_details_v2)
