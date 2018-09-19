import unittest
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data


class ShapeReducerDBSCANBadKeywords(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_no_keyword(self):
        '''Test error is raised if no keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data([])

    def test_bad_keyword(self):
        '''Test error is raised if a bad keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data([], shape='bad_shape')
