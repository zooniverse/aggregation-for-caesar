import unittest
import json
import urllib
import copy
from panoptes_aggregation.running_reducers.utilities import extract_in_data
from panoptes_aggregation.append_version import append_version

try:
    import flask
    OFFLINE = False
except ImportError:
    OFFLINE = True


def RunningReducerTestNoProcessing(
    reducer,
    extracted,
    reduced,
    name,
    kwargs={},
    network_kwargs={}
):
    class RunningReducerTestNoProcessing(unittest.TestCase):
        def setUp(self):
            self.maxDiff = None
            self.extracted = copy.deepcopy(extracted)
            self.reduced = copy.deepcopy(reduced)
            self.reduced_with_vesrion = copy.deepcopy(reduced)
            append_version(self.reduced_with_vesrion)

        def shortDescription(self):
            return '{0}: {1}'.format(name, self._testMethodDoc)

        def test_reducer(self):
            '''Test the offline reducer'''
            result = reducer(self.extracted, **kwargs, **network_kwargs)
            self.assertDictEqual(result, self.reduced_with_vesrion)

        @unittest.skipIf(OFFLINE, 'Installed in offline mode')
        def test_request(self):
            '''Test the online reducer'''
            request_kwargs = {
                'data': json.dumps(extract_in_data(self.extracted, **network_kwargs)),
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

    return RunningReducerTestNoProcessing
