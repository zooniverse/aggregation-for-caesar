from panoptes_aggregation.reducers.rectangle_reducer import rectangle_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0],
            'T0_tool0_details': [
                [
                    {'0': 1},
                    {'1': 1, '0': 1},
                    {'value': [
                        {'option-1': 1},
                        {'option-2': 1},
                        {'None': 1}
                    ]},
                    'No extractor for this subtask type'
                ],
                [
                    {'1': 1},
                    {'0': 1},
                    {'value': [
                        {'option-3': 1},
                        {'option-4': 1},
                        {'option-5': 1}
                    ]},
                    'No extractor for this subtask type'
                ],
            ],
            'T0_tool1_x': [500.0],
            'T0_tool1_y': [500.0],
            'T0_tool1_width': [10.0],
            'T0_tool1_height': [20.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0],
            'T0_tool0_details': [
                [
                    {'1': 1},
                    {'2': 1, '0': 1},
                    {'value': [
                        {'option-1': 1},
                        {'option-2': 1},
                        {'option-3': 1}
                    ]},
                    'No extractor for this subtask type'
                ],
                [
                    {'1': 1},
                    {'1': 1},
                    {'value': [
                        {'option-1': 1},
                        {'option-4': 1},
                        {'option-5': 1}
                    ]},
                    'No extractor for this subtask type'
                ]
            ],
            'T0_tool1_x': [500.0],
            'T0_tool1_y': [500.0],
            'T0_tool1_width': [10.0],
            'T0_tool1_height': [20.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [500.0],
            'T0_tool1_y': [500.0],
            'T0_tool1_width': [10.0],
            'T0_tool1_height': [20.0]
        }
    }
]

reduced_data = {
    'frame0': {
        'T0_tool0_rec_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rec_height': [20.0, 8.0, 20.0, 8.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [20.0, 8.0],
        'T0_tool0_details': [
            [
                {'0': 1},
                {'1': 1, '0': 1},
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'None': 1}
                ]},
                'No extractor for this subtask type'
            ],
            [
                {'1': 1},
                {'0': 1},
                {'value': [
                    {'option-3': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]},
                'No extractor for this subtask type'
            ],
            [
                {'1': 1},
                {'2': 1, '0': 1},
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'option-3': 1}
                ]},
                'No extractor for this subtask type'
            ],
            [
                {'1': 1},
                {'1': 1},
                {'value': [
                    {'option-1': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]},
                'No extractor for this subtask type'
            ]
        ],
        'T0_tool0_clusters_details': [
            [
                {'0': 1, '1': 1},
                {'1': 1, '2': 1, '0': 2},
                {'value': [
                    {'option-1': 2},
                    {'option-2': 2},
                    {'None': 1, 'option-3': 1}
                ]},
                'No reducer for this subtask type'
            ],
            [
                {'1': 2},
                {'0': 1, '1': 1},
                {'value': [
                    {'option-3': 1, 'option-1': 1},
                    {'option-4': 2},
                    {'option-5': 2}
                ]},
                'No reducer for this subtask type'
            ]
        ],
        'T0_tool1_rec_x': [500.0, 500.0, 500.0],
        'T0_tool1_rec_y': [500.0, 500.0, 500.0],
        'T0_tool1_rec_width': [10.0, 10.0, 10.0],
        'T0_tool1_rec_height': [20.0, 20.0, 20.0],
        'T0_tool1_cluster_labels': [0, 0, 0],
        'T0_tool1_clusters_count': [3],
        'T0_tool1_clusters_x': [500.0],
        'T0_tool1_clusters_y': [500.0],
        'T0_tool1_clusters_width': [10.0],
        'T0_tool1_clusters_height': [20.0]
    }
}

TestSubtaskReducer = ReducerTestNoProcessing(
    rectangle_reducer,
    extracted_data,
    reduced_data,
    'Test subtask reducer',
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_tool0': [
                'question_reducer',
                'question_reducer',
                'dropdown_reducer',
                None
            ]
        }
    }
)
