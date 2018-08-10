import copy
import unittest
import json
import numpy as np
import urllib
from panoptes_aggregation.extractors.test_utils import annotation_by_task

try:
    import flask
    OFFLINE = False
except ImportError:
    OFFLINE = True


def ExtractorTest(function, classification, expected, name, blank_extract={}, kwargs={}, test_type='assertDictEqual'):
    class ExtractorTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_extract(self):
            '''Test the offline extract function'''
            result = function(annotation_by_task(classification), **kwargs)
            if test_type == 'assertDictEqual':
                self.assertDictEqual(dict(result), expected)
            else:
                self.__getattribute__(test_type)(result, expected)

        def test_blank(self):
            '''Test a blank annotation'''
            blank = {'annotations': {'ST': []}}
            kwargs_blank = copy.deepcopy(kwargs)
            kwargs_blank['task'] = 'ST'
            result = function(blank, **kwargs_blank)
            if test_type == 'assertDictEqual':
                self.assertDictEqual(dict(result), blank_extract)
            else:
                self.__getattribute__(test_type)(result, blank_extract)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online extract function'''
            request_kwargs = {
                'data': json.dumps(annotation_by_task(classification)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = function(flask.request)
                if test_type == 'assertDictEqual':
                    self.assertDictEqual(dict(result), expected)
                else:
                    self.__getattribute__(test_type)(result, expected)

    return ExtractorTest


def TextExtractorTest(function, classification, expected, name, blank_extract={}, kwargs={}):
    class TextExtractorTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_extract(self):
            '''Test the offline extract function'''
            result = function(annotation_by_task(classification), **kwargs)
            for i in expected.keys():
                with self.subTest(i=i):
                    self.assertIn(i, result)
                    for j in expected[i].keys():
                        with self.subTest(i=j):
                            self.assertIn(j, result[i])
                            if j == 'slope':
                                np.testing.assert_allclose(result[i][j], expected[i][j], atol=1e-5)
                            else:
                                self.assertEqual(result[i][j], expected[i][j])

        def test_blank(self):
            '''Test a blank annotation'''
            blank = {'annotations': {'ST': []}}
            kwargs_blank = copy.deepcopy(kwargs)
            kwargs_blank['task'] = 'ST'
            result = function(blank, **kwargs_blank)
            self.assertDictEqual(dict(result), blank_extract)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online extract function'''
            request_kwargs = {
                'data': json.dumps(annotation_by_task(classification)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = function(flask.request)
                for i in expected.keys():
                    with self.subTest(i=i):
                        self.assertIn(i, result)
                        for j in expected[i].keys():
                            with self.subTest(i=j):
                                self.assertIn(j, result[i])
                                if j == 'slope':
                                    np.testing.assert_allclose(result[i][j], expected[i][j], atol=1e-5)
                                else:
                                    self.assertEqual(result[i][j], expected[i][j])

    return TextExtractorTest
