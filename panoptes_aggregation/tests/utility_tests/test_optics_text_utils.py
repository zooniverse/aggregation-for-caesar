import unittest
import numpy as np
from panoptes_aggregation.reducers import optics_text_utils

data = [
    {
        'x': [1, 5],
        'y': [1, 1],
        'text': ['This is   some [underline]test  text[/underline]'],
        'gold_standard': False
    },
    {
        'x': [1, 3],
        'y': [1, 1],
        'text': ['This is some test text'],
        'gold_standard': False
    },
    {
        'x': [1, 5],
        'y': [1, 3],
        'text': ['This is some test text'],
        'gold_standard': False
    },
    {
        'x': [1, 5],
        'y': [1, 1],
        'text': ['This is some test test'],
        'gold_standard': False
    },
]


class TextOpticsTextUtils(unittest.TestCase):
    def test_strip_tags(self):
        '''Test strip tags'''
        s = 'This is   some [underline]test  text[/underline]'
        expected = 'This is some test text'
        result = optics_text_utils.strip_tags(s)
        self.assertEqual(result, expected)

    def test_metric_same_point(self):
        '''Test metric with same point'''
        result = optics_text_utils.metric([0, 0], [0, 0], data_in=data)
        self.assertEqual(result, 0)

    def test_metric_same_user(self):
        '''Test metric with same point'''
        result = optics_text_utils.metric([0, 0], [1, 0], data_in=data)
        self.assertEqual(result, np.inf)

    def test_metric_distances(self):
        '''Test metric distances'''
        pair_list = [
            [[0, 0], [1, 1]],
            [[0, 0], [2, 1]],
            [[0, 0], [3, 1]]
        ]
        expected_distances = [
            2,
            2,
            1
        ]
        for i in range(len(pair_list)):
            with self.subTest(i=i):
                a, b = pair_list[i]
                result = optics_text_utils.metric(a, b, data_in=data)
                self.assertEqual(result, expected_distances[i])

    def test_get_min_samples(self):
        '''Test auto values for min_samples'''
        number_users = [2, 7, 11, 16, 21, 24, 40]
        min_samples = [2, 3, 4, 5, 5, 6, 10]
        for i in range(len(number_users)):
            with self.subTest(i=i):
                result = optics_text_utils.get_min_samples(number_users[i])
                self.assertEqual(result, min_samples[i])

    def test_remove_user_duplication(self):
        '''Test removing duplicate users within a cluster'''
        labels = np.array([0, 0, 1, 1, 1, 2, 2])
        core_distances = np.array([0.5, 0, 0, 1, 2, 0, 0.5])
        users = np.array([0, 0, 0, 1, 1, 0, 1])
        expected = np.array([-1, 0, 1, 1, -1, 2, 2])
        result = optics_text_utils.remove_user_duplication(
            labels,
            core_distances,
            users
        )
        np.testing.assert_array_equal(result, expected)

    def test_cluster_of_one(self):
        '''Test cluster of one'''
        X = [
            [0, 0],
            [1, 0]
        ]
        user_ids = [
            0
        ]
        ext_index = [0, 0]
        expected = [
            {
                'clusters_x': [1, 5],
                'clusters_y': [1, 1],
                'clusters_text': [
                    ['This'],
                    ['is'],
                    ['some'],
                    ['[underline]test'],
                    ['text[/underline]']
                ],
                'number_views': 1,
                'line_slope': 0.0,
                'consensus_score': 1.0,
                'user_ids': [0],
                'extract_index': [0],
                'gold_standard': [False]
            },
            {
                'clusters_x': [1, 3],
                'clusters_y': [1, 1],
                'clusters_text': [
                    ['This'],
                    ['is'],
                    ['some'],
                    ['test'],
                    ['text']
                ],
                'number_views': 1,
                'line_slope': 0.0,
                'consensus_score': 1.0,
                'user_ids': [0],
                'extract_index': [0],
                'gold_standard': [False]
            }
        ]
        result = optics_text_utils.cluster_of_one(X, data, user_ids, ext_index)
        self.assertCountEqual(result, expected)

    def test_order_lines(self):
        '''Test order lines function returns a list'''
        frame = [
            {
                'clusters_x': [1, 5],
                'clusters_y': [2, 2],
                'clusters_text': [
                    ['This'],
                    ['is'],
                    ['some'],
                    ['[underline]test'],
                    ['text[/underline]']
                ],
                'number_views': 1,
                'line_slope': 0.0,
                'consensus_score': 1.0,
                'user_ids': [0],
                'gold_standard': [False]
            }
        ]
        result = optics_text_utils.order_lines(frame)
        self.assertIsInstance(result, list)

    def test_remove_nans(self):
        '''Test remove nans'''
        input = [np.nan, 1, 2, 3, np.nan]
        expected = [None, 1, 2, 3, None]
        result = optics_text_utils.remove_nans(input)
        self.assertEquals(result, expected)


if __name__ == '__main__':
    unittest.main()
