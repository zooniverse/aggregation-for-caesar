import unittest
import json
import urllib
import copy
import numpy as np
from collections import OrderedDict
from panoptes_aggregation.reducers.utilities import extract_in_data
from panoptes_aggregation.append_version import append_version
from panoptes_aggregation.csv_utils import find_non_built_in_data_types

try:
    import flask
    OFFLINE = False
except ImportError:
    OFFLINE = True


def cast_to_dict(result):
    if isinstance(result, list):
        result_out_list = []
        for r in result:
            if isinstance(r, OrderedDict):
                result_out = dict(r)
            else:
                result_out = r

            for key in result_out.keys():
                if isinstance(result_out[key], OrderedDict):
                    result_out[key] = cast_to_dict(result_out[key])
            result_out_list.append(result_out)
        return result_out_list
    else:
        if isinstance(result, OrderedDict):
            result_out = dict(result)
        else:
            result_out = result

        for key in result_out.keys():
            if isinstance(result_out[key], OrderedDict):
                result_out[key] = cast_to_dict(result_out[key])
    return result_out


def round_dict(dictionary, ndigits):
    if isinstance(dictionary, dict):
        return {key: round_dict(value, ndigits) for key, value in dictionary.items()}
    elif isinstance(dictionary, list):
        return [round_dict(value, ndigits) for value in dictionary]
    elif isinstance(dictionary, float):
        return round(dictionary, ndigits)
    return dictionary


def ReducerTest(
    reducer,
    processer,
    extracted,
    processed,
    reduced,
    name,
    pkwargs={},
    okwargs={},
    kwargs={},
    network_kwargs={},
    processed_type='dict',
    add_version=True,
    output_kwargs=False,
    test_name=None,
    round=None
):
    # pkwargs: keywords passed into the process_data function
    # okwargs: keywords only passed into the _original function
    # kwargs: keywords passed into all steps
    # network_kwargs: keywords passed to the function but included along side `data` in the network request
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            if add_version:
                append_version(self.extracted_with_version)
            self.processed = copy.deepcopy(processed)
            if isinstance(reduced, list):
                self.reduction_is_list = True
            else:
                self.reduction_is_list = False
            self.reduced = copy.deepcopy(reduced)
            self.reduced_no_params = copy.deepcopy(reduced)
            if output_kwargs:
                if isinstance(self.reduced_no_params, list):
                    for r in self.reduced_no_params:
                        del r['parameters']
                else:
                    del self.reduced_no_params['parameters']
            self.reduced_with_version = copy.deepcopy(reduced)
            append_version(self.reduced_with_version)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_process_data(self):
            '''Test data processing function'''
            result = processer(self.extracted, **pkwargs)
            if processed_type == 'dict':
                result = cast_to_dict(result)
                if round:
                    result = round_dict(result, round)
                self.assertDictEqual(result, self.processed)
            else:
                self.assertCountEqual(result, self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original(self.processed, **okwargs, **kwargs, **network_kwargs)
            if self.reduction_is_list is True:
                for i, result_item in enumerate(result):
                    result_item = cast_to_dict(result_item)
                    if round is not None:
                        result_item = round_dict(result_item, round)
                    self.assertCountEqual(result_item, self.reduced_no_params[i])
            else:
                result = cast_to_dict(result)
                if round is not None:
                    result = round_dict(result, round)
                self.assertDictEqual(result, self.reduced_no_params)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs, **pkwargs, **network_kwargs)
            if self.reduction_is_list is True:
                for i, result_item in enumerate(result):
                    result_item = cast_to_dict(result_item)
                    if round is not None:
                        result_item = round_dict(result_item, round)
                    self.assertCountEqual(result_item, self.reduced_with_version[i])
            else:
                result = cast_to_dict(result)
                if round is not None:
                    result = round_dict(result, round)
                self.assertDictEqual(result, self.reduced_with_version)

        def test_reducer_data_types(self):
            '''Test the dictionary only contains built-in or nan data types'''
            result = reducer(self.extracted_with_version, **kwargs, **pkwargs, **network_kwargs)
            non_built_in_locations = find_non_built_in_data_types(result)
            expected = {}
            self.assertDictEqual(non_built_in_locations, expected)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version, **network_kwargs)),
                'content_type': 'application/json'
            }
            all_kwargs = dict(kwargs, **pkwargs)
            if len(all_kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(all_kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                if self.reduction_is_list is True:
                    for i, result_item in enumerate(result):
                        result_item = cast_to_dict(result_item)
                        if round is not None:
                            result_item = round_dict(result_item, round)
                        self.assertCountEqual(result_item, self.reduced_with_version[i])
                else:
                    result = reducer(self.extracted_with_version, **kwargs, **pkwargs, **network_kwargs)
                    result = cast_to_dict(result)
                    if round is not None:
                        result = round_dict(result, round)
                    self.assertDictEqual(result, self.reduced_with_version)

    if test_name is None:
        test_name = '_'.join(name.split())
    ReducerTest.__name__ = test_name
    ReducerTest.__qualname__ = test_name
    return ReducerTest


def ReducerTestNoProcessing(
    reducer,
    extracted,
    reduced,
    name,
    kwargs={},
    network_kwargs={},
    test_name=None,
    round=None
):
    class ReducerTestNoProcessing(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_version = copy.deepcopy(reduced)
            append_version(self.reduced_with_version)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs, **network_kwargs)
            result = cast_to_dict(result)
            if round is not None:
                result = round_dict(result, round)
            self.assertDictEqual(result, self.reduced_with_version)

        def test_reducer_data_types(self):
            '''Test the dictionary only contains built-in or nan data types'''
            result = reducer(self.extracted_with_version, **kwargs, **network_kwargs)
            non_built_in_locations = find_non_built_in_data_types(result)
            expected = {}
            self.assertDictEqual(non_built_in_locations, expected)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online reducer'''
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version, **network_kwargs)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                result = cast_to_dict(result)
                if round is not None:
                    result = round_dict(result, round)
                self.assertDictEqual(result, self.reduced_with_version)

    if test_name is None:
        test_name = '_'.join(name.split())
    ReducerTestNoProcessing.__name__ = test_name
    ReducerTestNoProcessing.__qualname__ = test_name
    return ReducerTestNoProcessing


def ReducerTestPoints(
    reducer,
    processer,
    extracted,
    processed,
    reduced,
    name,
    kwargs={},
    network_kwargs={},
    atol=2,
    test_name=None
):
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_version = copy.deepcopy(reduced)
            append_version(self.reduced_with_version)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def assertPoints(self, result, reduced):
            for i in result.keys():
                with self.subTest(i=i):
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(j=j):
                                try:
                                    np.testing.assert_allclose(result[i][j], reduced[i][j], atol=atol)
                                except TypeError:
                                    self.assertEqual(result[i][j], reduced[i][j])
                    else:
                        try:
                            np.testing.assert_allclose(result[i], reduced[i], atol=atol)
                        except TypeError:
                            self.assertEqual(result[i], reduced[i])

        def test_process_data(self):
            '''Test data processing function'''
            result = processer(self.extracted)
            self.assertDictEqual(cast_to_dict(result), self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original(self.processed, **kwargs, **network_kwargs)
            self.assertPoints(result, self.reduced)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs, **network_kwargs)
            self.assertPoints(result, self.reduced_with_version)

        def test_keys(self):
            '''Test the keys match up'''
            result = reducer(self.extracted_with_version, **kwargs, **network_kwargs)
            for i in self.reduced_with_version.keys():
                with self.subTest(i=i):
                    self.assertIn(i, result)
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(j=j):
                                self.assertIn(j, result[i])

        def test_reducer_data_types(self):
            '''Test the dictionary only contains built-in or nan data types'''
            result = reducer(self.extracted_with_version, **kwargs, **network_kwargs)
            non_built_in_locations = find_non_built_in_data_types(result)
            expected = {}
            self.assertDictEqual(non_built_in_locations, expected)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version, **network_kwargs)),
                'content_type': 'application/json'
            }
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertPoints(result, self.reduced_with_version)

    if test_name is None:
        test_name = '_'.join(name.split())
    ReducerTest.__name__ = test_name
    ReducerTest.__qualname__ = test_name
    return ReducerTest
