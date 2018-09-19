from panoptes_aggregation.reducers.shape_reducer_dbscan import shape_reducer_dbscan
from .base_test_class import ReducerTestNoProcessing

eytracted_data = [
    {
        'frame0': {
            'T0_tool0_y': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool1_y': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool1_y': [0.0, 100.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_y': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_y': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool0_y': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'fullWidthLine',
    'frame0': {
        'T0_tool0': [
            (0.0),
            (100.0),
            (0.0),
            (100.0)
        ],
        'T0_tool1': [
            (0.0),
            (100.0),
            (0.0),
            (100.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0)
        ],
        'T0_tool1': [
            (50.0),
            (50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_fullWidthLine_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool1_fullWidthLine_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_y': [0.0, 100.0]
    },
    'frame1': {
        'T0_tool0_fullWidthLine_y': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_fullWidthLine_y': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_y': [50.0]
    }
}

TestShapeReducerFullWidthLine = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    eytracted_data,
    reduced_data,
    'Test shape fullWidthLine reducer',
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'shape': 'fullWidthLine'
    }
)
