from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data, shape_reducer_dbscan
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_r': [50.0, 10.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_r': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_r': [50.0, 10.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_r': [10.0, 50.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_r': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_r': [10.0, 50.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_r': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'circle',
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0),
            (100.0, 100.0, 10.0),
            (0.0, 0.0, 50.00),
            (100.0, 100.0, 10.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0),
            (100.0, 0.0, 50.0),
            (0.0, 100.0, 10.0),
            (100.0, 0.0, 50.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_circle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_circle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_circle_r': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_r': [50.0, 10.0],
        'T0_tool1_circle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_circle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_circle_r': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_r': [10.0, 50.0]
    },
    'frame1': {
        'T0_tool0_circle_x': [20.0],
        'T0_tool0_circle_y': [20.0],
        'T0_tool0_circle_r': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_circle_x': [50.0, 50.0],
        'T0_tool1_circle_y': [50.0, 50.0],
        'T0_tool1_circle_r': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_r': [50.0]
    }
}

TestShapeReducerCircle = ReducerTest(
    shape_reducer_dbscan,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape circle reducer',
    pkwargs={'shape': 'circle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)
