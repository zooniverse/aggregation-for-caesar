from panoptes_aggregation import reducers
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_subtask0': [
                {
                    'text': 'this is some test text',
                    'gold_standard': True
                },
                {
                    'text': 'more text',
                    'gold_standard': True
                }
            ]
        }
    },
    {'classifier_version': '2.0'},
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_subtask0': [
                {
                    'text': 'this is some text text',
                    'gold_standard': False
                },
                {
                    'text': 'more test',
                    'gold_standard': False
                }
            ]
        }
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
        3,
        2
    ]
}

reduced_data = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_tool0_point_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_point_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_subtask0': [
            {
                'text': 'this is some test text',
                'gold_standard': True
            },
            {
                'text': 'more text',
                'gold_standard': True
            },
            {
                'text': 'this is some text text',
                'gold_standard': False
            },
            {
                'text': 'more test',
                'gold_standard': False
            }
        ],
        'T0_tool0_subtask0_clusters': [
            {
                'aligned_text': [
                    ['this', 'this'],
                    ['is', 'is'],
                    ['some', 'some'],
                    ['test', 'text'],
                    ['text', 'text']
                ],
                'number_views': 2,
                'consensus_score': 1.8,
                'consensus_text': 'this is some test text',
                'gold_standard': [True, False],
                'user_ids': [1, 2]
            },
            {
                'aligned_text': [
                    ['more', 'more'],
                    ['text', 'test']
                ],
                'number_views': 2,
                'consensus_score': 1.5,
                'consensus_text': 'more text',
                'gold_standard': [True, False],
                'user_ids': [1, 2]
            }
        ]
    }
}

TestTextSubtaskReducerV2 = ReducerTestNoProcessing(
    reducers.shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test text subtask reducer with classifier v2 extracts',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'point',
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_tool0_subtask0': 'text_reducer'
        }
    },
    test_name='TestTextSubtaskReducerV2'
)
