from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data, shape_reducer_dbscan
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_width': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_width': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_width': [0.0, 100.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_width': [100.0, 0.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_width': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_width': [100.0, 0.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_width': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'column',
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0),
            (100.0, 100.0),
            (0.0, 0.0),
            (100.0, 100.0)
        ],
        'T0_tool1': [
            (0.0, 100.0),
            (100.0, 0.0),
            (0.0, 100.0),
            (100.0, 0.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0),
            (50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_column_width': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_width': [0.0, 100.0],
        'T0_tool1_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_column_width': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_width': [100.0, 0.0]
    },
    'frame1': {
        'T0_tool0_column_x': [20.0],
        'T0_tool0_column_width': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_column_x': [50.0, 50.0],
        'T0_tool1_column_width': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_width': [50.0]
    }
}

TestShapeReducerColumn = ReducerTest(
    shape_reducer_dbscan,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape column reducer',
    pkwargs={'shape': 'column'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)
