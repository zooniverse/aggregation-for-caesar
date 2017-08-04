import unittest
from panoptes_aggregation.reducers import process_kwargs

DEFAULTS = {
    'a': {'default': 5.0, 'type': float},
    'b': {'default': 3, 'type': int},
    'c': {'default': 'hi', 'type': str},
}

expected_default = {
    'a': 5.0,
    'b': 3,
    'c': 'hi'
}


class TestProcessKwargs(unittest.TestCase):
    def test_defaults(self):
        kwargs = {}
        result = process_kwargs(kwargs, DEFAULTS)
        self.assertDictEqual(result, expected_default)

    def test_setting_value(self):
        # make sure value sets as correct type
        kwargs = {'a': '10'}
        expected = {
            'a': 10.0,
            'b': 3,
            'c': 'hi'
        }
        result = process_kwargs(kwargs, DEFAULTS)
        self.assertDictEqual(result, expected)

    def test_wrong_type(self):
        # make sure default is used with bad keywords are passed in
        kwargs = {'b': '10.5'}
        result = process_kwargs(kwargs, DEFAULTS)
        self.assertDictEqual(result, expected_default)

    def test_wrong_key(self):
        # make sure invalid keywords are not passed in
        kwargs = {'random': 'set'}
        result = process_kwargs(kwargs, DEFAULTS)
        self.assertDictEqual(result, expected_default)


if __name__ == '__main__':
    unittest.main()
