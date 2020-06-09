from panoptes_aggregation.reducers.shape_reducer_dbscan import shape_reducer_dbscan
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {'frame0': {
        'T0_tool0_x': [0.0, 100.0],
        'T0_tool0_y': [0.0, 100.0],
        'T0_tool0_width': [50.0, 10.0],
        'T0_tool0_height': [20.0, 8.0],
        'T0_tool0_details': [
            [{
                'text': 'this is some test text',
                'gold_standard': True
            }],
            [{
                'text': 'more text',
                'gold_standard': True
            }]
        ]
    }},
    {},
    {'frame0': {
        'T0_tool0_x': [0.0, 100.0],
        'T0_tool0_y': [0.0, 100.0],
        'T0_tool0_width': [50.0, 10.0],
        'T0_tool0_height': [20.0, 8.0],
        'T0_tool0_details': [
            [{
                'text': 'this is some text text',
                'gold_standard': False
            }],
            [{
                'text': 'more test',
                'gold_standard': False
            }]
        ]
    }}
]

kwargs_extra_data = {
    'user_id': [
        1,
        3,
        2
    ]
}

reduced_data = {
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [20.0, 8.0, 20.0, 8.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [20.0, 8.0],
        'T0_tool0_details': [
            [{
                'text': 'this is some test text',
                'gold_standard': True
            }],
            [{
                'text': 'more text',
                'gold_standard': True
            }],
            [{
                'text': 'this is some text text',
                'gold_standard': False
            }],
            [{
                'text': 'more test',
                'gold_standard': False
            }]
        ],
        'T0_tool0_clusters_details': [
            [{
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
            }],
            [{
                'aligned_text': [
                    ['more', 'more'],
                    ['text', 'test']
                ],
                'number_views': 2,
                'consensus_score': 1.5,
                'consensus_text': 'more text',
                'gold_standard': [True, False],
                'user_ids': [1, 2]
            }]
        ]
    }
}

TestTextSubtaskReducer = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test text subtask reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_tool0': ['text_reducer']
        }
    },
    test_name='TestTextSubtaskReducer'
)
