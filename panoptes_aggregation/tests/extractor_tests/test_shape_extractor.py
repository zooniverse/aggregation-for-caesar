import unittest
from panoptes_aggregation import extractors
from panoptes_aggregation.extractors.utilities import annotation_by_task

classification = {
    'annotations': [
        {
            'task': 'T0',
            'value': [
                {
                    'tool': 0,
                    'frame': 0
                }
            ]
        }
    ]
}


class ShapeExtractorBadKeywords(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_no_keyword(self):
        '''Test error is raised if no keyword is used for shape'''
        with self.assertRaises(KeyError):
            extractors.shape_extractor(
                annotation_by_task(classification)
            )

    def test_bad_keyword(self):
        '''Test error is raised if a bad keyword is used for shape'''
        with self.assertRaises(KeyError):
            extractors.shape_extractor(
                annotation_by_task(classification),
                shape='bad_shape'
            )
