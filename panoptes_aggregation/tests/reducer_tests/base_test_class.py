import unittest
import json
import urllib
import copy
import numpy as np
from collections import OrderedDict
from panoptes_aggregation.reducers.utilities import extract_in_data
from panoptes_aggregation.append_version import append_version

try:
    import flask
    OFFLINE = False
except ImportError:
    OFFLINE = True


def cast_to_dict(result):
    if isinstance(result, OrderedDict):
        result_out = dict(result)
    else:
        result_out = result
    for key in result_out.keys():
        if isinstance(result_out[key], OrderedDict):
            result_out[key] = cast_to_dict(result_out[key])
    return result_out


def ReducerTest(reducer, processer, extracted, processed, reduced, name, pkwargs={}, okwargs={}, kwargs={}, processed_type='dict'):
    # pkwargs: keywords passed into the process_data funciton
    # okwargs: keywords only passed into the _original function
    # kwargs: keywords passed into all steps
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_vesrion = copy.deepcopy(reduced)
            append_version(self.reduced_with_vesrion)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_process_data(self):
            '''Test data processing function'''
            result = processer(self.extracted, **pkwargs)
            if processed_type == 'dict':
                self.assertDictEqual(cast_to_dict(result), self.processed)
            else:
                self.assertCountEqual(result, self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original(self.processed, **okwargs, **kwargs)
            self.assertDictEqual(cast_to_dict(result), self.reduced)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs, **pkwargs)
            self.assertDictEqual(cast_to_dict(result), self.reduced_with_vesrion)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version)),
                'content_type': 'application/json'
            }
            all_kwargs = dict(kwargs, **pkwargs)
            if len(all_kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(all_kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertDictEqual(cast_to_dict(result), self.reduced_with_vesrion)

    return ReducerTest


def ReducerTestNoProcessing(reducer, extracted, reduced, name, kwargs={}):
    class ReducerTestNoProcessing(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_vesrion = copy.deepcopy(reduced)
            append_version(self.reduced_with_vesrion)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs)
            self.assertDictEqual(result, self.reduced_with_vesrion)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online reducer'''
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertDictEqual(result, self.reduced_with_vesrion)

    return ReducerTestNoProcessing


def ReducerTestSurvey(reducer, processer, extracted, processed, reduced, name):
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_vesrion = copy.deepcopy(reduced)
            append_version(self.reduced_with_vesrion)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_process_data(self):
            '''Test data processing function'''
            result, count = processer(self.extracted)
            self.assertEqual(count, len(self.extracted))
            self.assertDictEqual(result, self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original((self.processed, len(self.extracted)))
            self.assertCountEqual(result, self.reduced)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version)
            self.assertCountEqual(result, self.reduced_with_vesrion)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version)),
                'content_type': 'application/json'
            }
            with app.test_request_context(**request_kwargs):
                result = reducer(flask.request)
                self.assertCountEqual(result, self.reduced_with_vesrion)

    return ReducerTest


def ReducerTestPoints(reducer, processer, extracted, processed, reduced, name, kwargs={}, atol=2):
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.extracted_with_version = copy.deepcopy(extracted)
            append_version(self.extracted_with_version)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_vesrion = copy.deepcopy(reduced)
            append_version(self.reduced_with_vesrion)

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
            result = reducer._original(self.processed, **kwargs)
            self.assertPoints(result, self.reduced)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted_with_version, **kwargs)
            self.assertPoints(result, self.reduced_with_vesrion)

        def test_keys(self):
            '''Test the keys match up'''
            result = reducer(self.extracted_with_version, **kwargs)
            for i in self.reduced_with_vesrion.keys():
                with self.subTest(i=i):
                    self.assertIn(i, result)
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(j=j):
                                self.assertIn(j, result[i])

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted_with_version)),
                'content_type': 'application/json'
            }
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertPoints(result, self.reduced_with_vesrion)

    return ReducerTest
