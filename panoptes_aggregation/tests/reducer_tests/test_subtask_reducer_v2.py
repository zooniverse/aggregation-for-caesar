from panoptes_aggregation import reducers
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x': [0.0, 100.0],
            'T0_toolIndex0_y': [0.0, 100.0],
            'T0_toolIndex0_subtask0': [
                {'0': 1},
                {'1': 1}
            ],
            'T0_toolIndex0_subtask1': [
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'None': 1}
                ]},
                {'value': [
                    {'option-3': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]}
            ],
            'T0_toolIndex1_x': [500.0],
            'T0_toolIndex1_y': [500.0],
            'T0_toolIndex1_subtask0': [
                {'1': 1}
            ],
            'T0_toolIndex1_subtask1': [
                {'value': [
                    {'option-3': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]}
            ]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x': [0.0, 100.0],
            'T0_toolIndex0_y': [0.0, 100.0],
            'T0_toolIndex0_subtask0': [
                {'1': 1},
                {'1': 1}
            ],
            'T0_toolIndex0_subtask1': [
                {'value': [
                    {'option-1': 1},
                    {'option-2': 1},
                    {'option-3': 1}
                ]},
                {'value': [
                    {'option-1': 1},
                    {'option-4': 1},
                    {'option-5': 1}
                ]}
            ],
            'T0_toolIndex1_x': [500.0],
            'T0_toolIndex1_y': [500.0],
            'T0_toolIndex1_subtask0': [
                {'1': 1}
            ],
            'T0_toolIndex1_subtask1': [
                {'value': [
                    {'option-1': 1},
                    {'option-3': 1},
                    {'option-5': 1}
                ]}
            ]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x': [500.0],
            'T0_toolIndex1_y': [500.0],
            'T0_toolIndex1_subtask0': [
                {'0': 1}
            ],
            'T0_toolIndex1_subtask1': [
                {'value': [
                    {'option-1': 1},
                    {'option-3': 1},
                    {'option-5': 1}
                ]}
            ]
        }
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        3
    ]
}

reduced_data = {
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0_point_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_point_y': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x': [0.0, 100.0],
        'T0_toolIndex0_clusters_y': [0.0, 100.0],
        'T0_toolIndex0_subtask0': [
            {'0': 1},
            {'1': 1},
            {'1': 1},
            {'1': 1}
        ],
        'T0_toolIndex0_subtask1': [
            {'value': [
                {'option-1': 1},
                {'option-2': 1},
                {'None': 1}
            ]},
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]},
            {'value': [
                {'option-1': 1},
                {'option-2': 1},
                {'option-3': 1}
            ]},
            {'value': [
                {'option-1': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]}
        ],
        'T0_toolIndex0_subtask0_clusters': [
            {'0': 1, '1': 1},
            {'1': 2}
        ],
        'T0_toolIndex0_subtask1_clusters': [
            {'value': [
                {'option-1': 2},
                {'option-2': 2},
                {'None': 1, 'option-3': 1}
            ]},
            {'value': [
                {'option-3': 1, 'option-1': 1},
                {'option-4': 2},
                {'option-5': 2}
            ]}
        ],
        'T0_toolIndex1_point_x': [500.0, 500.0, 500.0],
        'T0_toolIndex1_point_y': [500.0, 500.0, 500.0],
        'T0_toolIndex1_cluster_labels': [0, 0, 0],
        'T0_toolIndex1_clusters_count': [3],
        'T0_toolIndex1_clusters_x': [500.0],
        'T0_toolIndex1_clusters_y': [500.0],
        'T0_toolIndex1_subtask0': [
            {'1': 1},
            {'1': 1},
            {'0': 1}
        ],
        'T0_toolIndex1_subtask1': [
            {'value': [
                {'option-3': 1},
                {'option-4': 1},
                {'option-5': 1}
            ]},
            {'value': [
                {'option-1': 1},
                {'option-3': 1},
                {'option-5': 1}
            ]},
            {'value': [
                {'option-1': 1},
                {'option-3': 1},
                {'option-5': 1}
            ]}
        ],
        'T0_toolIndex1_subtask0_clusters': [
            {'0': 1, '1': 2}
        ],
        'T0_toolIndex1_subtask1_clusters': [
            {'value': [
                {'option-1': 2, 'option-3': 1},
                {'option-3': 2, 'option-4': 1},
                {'option-5': 3}
            ]}
        ]
    }
}

TestSubtaskReducerV2 = ReducerTestNoProcessing(
    reducers.shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test subtask reducer with classifier v2 extracts',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'point',
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_toolIndex0_subtask0': 'question_reducer',
            'T0_toolIndex0_subtask1': 'dropdown_reducer',
            'T0_toolIndex1_subtask0': 'question_reducer',
            'T0_toolIndex1_subtask1': 'dropdown_reducer'
        }
    },
    test_name='TestSubtaskReducerV2'
)

reduced_data_no_details = {
    'frame0': {
        'T0_toolIndex0_point_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_point_y': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x': [0.0, 100.0],
        'T0_toolIndex0_clusters_y': [0.0, 100.0],
        'T0_toolIndex1_point_x': [500.0, 500.0, 500.0],
        'T0_toolIndex1_point_y': [500.0, 500.0, 500.0],
        'T0_toolIndex1_cluster_labels': [0, 0, 0],
        'T0_toolIndex1_clusters_count': [3],
        'T0_toolIndex1_clusters_x': [500.0],
        'T0_toolIndex1_clusters_y': [500.0],
    }
}

TestSubtaskReducerV2NoDetails = ReducerTestNoProcessing(
    reducers.shape_reducer_dbscan,
    extracted_data,
    reduced_data_no_details,
    'Test subtask reducer with classifier v2 extracts',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'point',
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestSubtaskReducerV2NoDetails'
)
