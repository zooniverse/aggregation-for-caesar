import unittest
from collections import OrderedDict
import pandas
from pandas.util.testing import assert_frame_equal
import panoptes_aggregation.csv_utils as csv_utils

nested_data = {
    'classification_id': [1, 2, 3],
    'user_id': [1, 2, 3],
    'data': [
        {'a': 1, 'b': 0, 'c': {'d': 0, 'e': 1}},
        {'a': 0, 'b': 0, 'c': {'d': 1, 'e': 0}},
        {'a': 1, 'b': 1, 'c': {'d': 1, 'e': 1}}
    ]
}

flat_data = pandas.DataFrame({
    'classification_id': [1, 2, 3],
    'user_id': [1, 2, 3],
    'data.a': [1, 0, 1],
    'data.b': [0, 0, 1],
    'data.c.d': [0, 1, 1],
    'data.c.e': [1, 0, 1]
})

flat_row = flat_data.iloc[0]

expected_unflatten_renest = {'a': 1, 'b': 0, 'c': {'d': 0, 'e': 1}}
expected_unflatten = {'a': 1, 'b': 0, 'c.d': 0, 'c.e': 1}

json_data = pandas.DataFrame({
    'classification_id': [1, 2, 3, 4],
    'data.points': [
        '{"x": 1, "y": 1}',
        '{"x": 2, "y": 2}',
        '{"x": 3, "y": 3}',
        pandas.np.nan
    ],
    'data.text': ['how', 'are', 'you', pandas.np.nan]
})

unjson_data = pandas.DataFrame({
    'classification_id': [1, 2, 3, 4],
    'data.points': [
        {"x": 1, "y": 1},
        {"x": 2, "y": 2},
        {"x": 3, "y": 3},
        pandas.np.nan
    ],
    'data.text': ['how', 'are', 'you', pandas.np.nan]
})

unordered_data = pandas.DataFrame(OrderedDict((
    ('classification_id', [1, 2, 3]),
    ('data.c', [1, 2, 3]),
    ('data.b', [1, 2, 3]),
    ('data.a', [1, 2, 3]),
    ('data.choice', ['a', 'b', 'c'])
)))

ordered_data = pandas.DataFrame(OrderedDict((
    ('classification_id', [1, 2, 3]),
    ('data.choice', ['a', 'b', 'c']),
    ('data.a', [1, 2, 3]),
    ('data.b', [1, 2, 3]),
    ('data.c', [1, 2, 3])
)))


class TestCSVUtils(unittest.TestCase):
    def test_flatten_data(self):
        '''Test if nested `data` column flattened to many columns'''
        result = csv_utils.flatten_data(nested_data)
        assert_frame_equal(result, flat_data, check_like=True)

    def test_unflatten_data_renest(self):
        '''Test unflattening of data with the renest keyword'''
        result = csv_utils.unflatten_data(flat_row, renest=True)
        self.assertDictEqual(result, expected_unflatten_renest)

    def test_unflatten_data(self):
        '''Test unflattening of data with out the renest keyword'''
        result = csv_utils.unflatten_data(flat_row, renest=False)
        self.assertDictEqual(result, expected_unflatten)

    def test_unjson_dataframe(self):
        '''Test unjson dataframe with `nan` values'''
        csv_utils.unjson_dataframe(json_data)
        assert_frame_equal(json_data, unjson_data, check_like=True)

    def test_order_columns(self):
        '''Test order columns'''
        result = csv_utils.order_columns(unordered_data, front=['choice'])
        assert_frame_equal(result, ordered_data)
