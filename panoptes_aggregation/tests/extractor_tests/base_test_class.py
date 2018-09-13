import copy
import unittest
import json
import numpy as np
import urllib
from panoptes_aggregation.extractors.utilities import annotation_by_task
from panoptes_aggregation.append_version import append_version

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

        def assertTestType(self, result, expected):
            if test_type == 'assertDictEqual':
                self.assertDictEqual(dict(result), expected)
            else:
                self.__getattribute__(test_type)(result, expected)

        def test_extract(self):
            '''Test the offline extract function'''
            result = function(annotation_by_task(classification), **kwargs)
            append_version(expected)
            self.assertTestType(result, expected)

        def test_blank(self):
            '''Test a blank annotation'''
            blank = {'annotations': {'ST': []}}
            kwargs_blank = copy.deepcopy(kwargs)
            kwargs_blank['task'] = 'ST'
            result = function(blank, **kwargs_blank)
            append_version(blank_extract)
            self.assertTestType(result, blank_extract)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online extract function'''
            request_kwargs = {
                'data': json.dumps(annotation_by_task(classification)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            append_version(expected)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = function(flask.request)
                self.assertTestType(result, expected)

    return ExtractorTest


def TextExtractorTest(function, classification, expected, name, blank_extract={}, kwargs={}):
    class TextExtractorTest(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def assertTextExtractor(self, result, expected):
            for i in expected.keys():
                with self.subTest(i=i):
                    self.assertIn(i, result)
                    if isinstance(expected[i], dict):
                        for j in expected[i].keys():
                            with self.subTest(i=j):
                                self.assertIn(j, result[i])
                                if j == 'slope':
                                    np.testing.assert_allclose(result[i][j], expected[i][j], atol=1e-5)
                                else:
                                    self.assertEqual(result[i][j], expected[i][j])

        def test_extract(self):
            '''Test the offline extract function'''
            result = function(annotation_by_task(classification), **kwargs)
            append_version(expected)
            self.assertTextExtractor(result, expected)

        def test_blank(self):
            '''Test a blank annotation'''
            blank = {'annotations': {'ST': []}}
            kwargs_blank = copy.deepcopy(kwargs)
            kwargs_blank['task'] = 'ST'
            result = function(blank, **kwargs_blank)
            append_version(blank_extract)
            self.assertDictEqual(dict(result), blank_extract)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online extract function'''
            request_kwargs = {
                'data': json.dumps(annotation_by_task(classification)),
                'content_type': 'application/json'
            }
            app = flask.Flask(__name__)
            append_version(expected)
            if len(kwargs) > 0:
                url_params = '?{0}'.format(urllib.parse.urlencode(kwargs))
            else:
                url_params = ''
            with app.test_request_context(url_params, **request_kwargs):
                result = function(flask.request)
                self.assertTextExtractor(result, expected)

    return TextExtractorTest


def TextExtractorBadKeywordTest(function, classification, expected, name):
    class TextExtractorTestBadKeyword(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_bad_keyword(self):
            '''Test error is raised if a bad keyword is used for dot_freq'''
            with self.assertRaises(ValueError):
                function(annotation_by_task(classification), dot_freq='bad_keyword')

    return TextExtractorTestBadKeyword
