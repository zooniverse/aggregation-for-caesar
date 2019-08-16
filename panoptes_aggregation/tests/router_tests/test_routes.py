try:
    import panoptes_aggregation.routes as routes
    OFFLINE = False
except ImportError:
    OFFLINE = True
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import os
import panoptes_aggregation

mock_question_extractor = MagicMock()
mock_question_extractor.return_value = 'OK'
mock_extractors_dict = {
    'question_extractor': mock_question_extractor
}


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
class RouterTest(unittest.TestCase):
    def setUp(self):
        self.application = routes.make_application()
        self.ME = routes.MyEncoder()

    def route_exists(self, route, expected):
        with self.application.test_client() as client:
            response = client.get(route)
            self.assertEqual(response.status_code, 200)
            result = eval(response.data)
            self.assertEqual(result, expected)

    def test_home_route(self):
        '''Test home page returns version'''
        self.route_exists(
            '/',
            'Python extractors and reducers for panoptes aggregation. Code version {0}'.format(panoptes_aggregation.__version__)
        )

    def test_extractor_routes(self):
        '''Test all extractor routes exists'''
        for extractor_name in panoptes_aggregation.extractors.extractors.keys():
            with self.subTest(extractor=extractor_name):
                self.route_exists(
                    '/extractors/{0}'.format(extractor_name),
                    extractor_name
                )

    def test_reducer_routes(self):
        '''Test all reducer routes exists'''
        for reducer_name in panoptes_aggregation.reducers.reducers.keys():
            with self.subTest(reducer=reducer_name):
                self.route_exists(
                    '/reducers/{0}'.format(reducer_name),
                    reducer_name
                )

    def test_one_running_reducer_route(self):
        '''Test all running reducer routes exists'''
        for running_reducer_name in panoptes_aggregation.running_reducers.running_reducers.keys():
            with self.subTest(reducer=running_reducer_name):
                self.route_exists(
                    '/running_reducers/{0}'.format(running_reducer_name),
                    running_reducer_name
                )

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_docs_route(self):
        '''Test docs route works'''
        with self.application.test_client() as client:
            response = client.get('/docs')
            self.assertEqual(response.status_code, 200)

    def test_post_to_route(self):
        '''Test POST to route works'''
        with patch.dict('panoptes_aggregation.routes.extractors.extractors', mock_extractors_dict):
            with routes.make_application().test_client() as client:
                response = client.post('/extractors/question_extractor')
                self.assertEqual(response.status_code, 200)

    def test_MyEncoder_int(self):
        '''Test MyEncoder converts numpy ints'''
        result = self.ME.default(np.int64(5))
        self.assertIsInstance(result, int)

    def test_MyEncoder_float(self):
        '''Test MyEncoder converts numpy floats'''
        result = self.ME.default(np.float64(5))
        self.assertIsInstance(result, float)

    def test_MyEncoder_array(self):
        '''Test MyEncoder converts numpy arrays'''
        result = self.ME.default(np.array([5]))
        self.assertIsInstance(result, list)

    def test_MyEncoder_other(self):
        '''Test MyEncoder passes all other data types to base to raise error'''
        with self.assertRaises(TypeError):
            self.ME.default('a')
