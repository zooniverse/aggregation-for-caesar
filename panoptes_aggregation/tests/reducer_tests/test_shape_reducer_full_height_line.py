from panoptes_aggregation.reducers.shape_reducer_dbscan import shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import shape_reducer_hdbscan
from .base_test_class import ReducerTestNoProcessing
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool1_x': [0.0, 100.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'fullHeightLine',
    'symmetric': False,
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
        'T0_tool0_fullHeightLine_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool1_fullHeightLine_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0]
    },
    'frame1': {
        'T0_tool0_fullHeightLine_x': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_fullHeightLine_x': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0]
    }
}

TestShapeReducerFullHeightLine = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test shape fullHeightLine reducer with DBSCAN',
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'shape': 'fullHeightLine'
    }
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1, 1, 1, 1]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [1, 1]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1, 1, 1, 1]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [1, 1]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1, 1]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1]

TestShapeReducerFullHeightLineHdbscan = ReducerTestNoProcessing(
    shape_reducer_hdbscan,
    extracted_data,
    reduced_data_hdbscan,
    'Test shape fullHeightLine reducer with HDBSCAN',
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True,
        'shape': 'fullHeightLine'
    }
)
