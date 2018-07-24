import unittest
import flask
import json
import urllib
import copy
import numpy as np
from panoptes_aggregation.reducers.test_utils import extract_in_data


def ReducerTest(reducer, processer, extracted, processed, reduced, name, pkwargs={}, okwargs={}, kwargs={}, processed_type='dict'):
    # pkwargs: keywords passed into the process_data funciton
    # okwargs: keywords only passed into the _original function
    # kwargs: keywords passed into all steps
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_process_data(self):
            '''Test data processing function'''
            result = processer(self.extracted, **pkwargs)
            if processed_type == 'dict':
                self.assertDictEqual(dict(result), self.processed)
            else:
                self.assertCountEqual(result, self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original(self.processed, **okwargs, **kwargs)
            self.assertDictEqual(dict(result), self.reduced)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted, **kwargs, **pkwargs)
            self.assertDictEqual(dict(result), self.reduced)

        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted)),
                'content_type': 'application/json'
            }
            all_kwargs = dict(kwargs, **pkwargs)
            if len(all_kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(all_kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertDictEqual(dict(result), self.reduced)

    return ReducerTest


def ReducerTestNoProcessing(reducer, extracted, reduced, name, kwargs={}):
    class ReducerTestNoProcessing(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(extracted, **kwargs)
            self.assertDictEqual(result, reduced)

        def test_request(self):
            '''Test the online reducer'''
            request_kwargs = {
                'data': json.dumps(extract_in_data(extracted)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                self.assertDictEqual(result, reduced)

    return ReducerTestNoProcessing


def ReducerTestSurvey(reducer, processer, extracted, processed, reduced, name):
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)

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
            result = reducer(self.extracted)
            self.assertCountEqual(result, self.reduced)

        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted)),
                'content_type': 'application/json'
            }
            with app.test_request_context(**request_kwargs):
                result = reducer(flask.request)
                self.assertCountEqual(result, self.reduced)

    return ReducerTest


def ReducerTestPoints(reducer, processer, extracted, processed, reduced, name, kwargs={}, atol=2):
    class ReducerTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.processed = copy.deepcopy(processed)
            self.reduced = copy.deepcopy(reduced)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_process_data(self):
            '''Test data processing function'''
            result = processer(self.extracted)
            self.assertDictEqual(dict(result), self.processed)

        def test_original_reducer(self):
            '''Test the reducer function starting with the processed data'''
            result = reducer._original(self.processed, **kwargs)
            for i in result.keys():
                with self.subTest(i=i):
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(i=j):
                                np.testing.assert_allclose(result[i][j], reduced[i][j], atol=atol)
                    else:
                        np.testing.assert_allclose(result[i], reduced[i], atol=atol)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted, **kwargs)
            for i in result.keys():
                with self.subTest(i=i):
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(i=j):
                                np.testing.assert_allclose(result[i][j], reduced[i][j], atol=atol)
                    else:
                        np.testing.assert_allclose(result[i], reduced[i], atol=atol)

        def test_keys(self):
            result = reducer(self.extracted, **kwargs)
            for i in reduced.keys():
                with self.subTest(i=i):
                    self.assertIn(i, result)
                    if isinstance(result[i], dict):
                        for j in result[i].keys():
                            with self.subTest(i=j):
                                self.assertIn(j, result[i])

        def test_reducer_request(self):
            '''Test the online reducer'''
            app = flask.Flask(__name__)
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted)),
                'content_type': 'application/json'
            }
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = reducer(flask.request)
                for i in result.keys():
                    with self.subTest(i=i):
                        if isinstance(result[i], dict):
                            for j in result[i].keys():
                                with self.subTest(i=j):
                                    np.testing.assert_allclose(result[i][j], reduced[i][j], atol=atol)
                        else:
                            np.testing.assert_allclose(result[i], reduced[i], atol=atol)

    return ReducerTest
