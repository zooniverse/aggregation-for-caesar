import unittest
from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan


class ShapeReducerDBSCANBadKeywords(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_no_keyword_dbscan(self):
        '''Test error is raised in DBSCAN if no keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_dbscan([])

    def test_bad_keyword_dbscan(self):
        '''Test error is raised in DBSCAN if a bad keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_dbscan([], shape='bad_shape')

    def test_bad_metric_keyword_dbscan(self):
        '''Test error is raised in DBSCAN if a bad metric keyword is used'''
        with self.assertRaises(ValueError):
            shape_reducer_dbscan([], metric_type='bad', user_id=[], shape='circle')

    def test_no_keyword_hdbscan(self):
        '''Test error is raised in HDBSCAN if no keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_hdbscan([])

    def test_bad_keyword_hdbscan(self):
        '''Test error is raised in HDBSCAN if a bad keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_hdbscan([], shape='bad_shape')

    def test_bad_metric_keyword_hdbscan(self):
        '''Test error is raised in HDBSCAN if a bad metric keyword is used'''
        with self.assertRaises(ValueError):
            shape_reducer_hdbscan([], metric_type='bad', user_id=[], shape='circle')

    def test_no_keyword_optics(self):
        '''Test error is raised in OPTICS if no keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_optics([])

    def test_bad_keyword_optics(self):
        '''Test error is raised in OPTICS if a bad keyword is used for shape'''
        with self.assertRaises(KeyError):
            process_data_optics([], shape='bad_shape')

    def test_bad_metric_keyword_optics(self):
        '''Test error is raised in OPTICS if a bad metric keyword is used'''
        with self.assertRaises(ValueError):
            shape_reducer_optics([], metric_type='bad', user_id=[], shape='circle')
