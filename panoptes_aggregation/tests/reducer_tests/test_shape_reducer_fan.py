from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_radius': [50.0, 10.0],
            'T0_tool0_spread': [60.0, 20.0],
            'T0_tool0_rotation': [1.0, 359.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_radius': [50.0],
            'T0_tool1_spread': [50.0],
            'T0_tool1_rotation': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_radius': [50.0, 10.0],
            'T0_tool0_spread': [60.0, 20.0],
            'T0_tool0_rotation': [359.0, 1.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_radius': [10.0, 50.0],
            'T0_tool1_spread': [50.0, 10.0],
            'T0_tool1_rotation': [1.0, 359.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_radius': [50.0],
            'T0_tool1_spread': [50.0],
            'T0_tool1_rotation': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_radius': [10.0, 50.0],
            'T0_tool1_spread': [50.0, 10.0],
            'T0_tool1_rotation': [359.0, 1.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_radius': [20.0],
            'T0_tool0_spread': [20.0],
            'T0_tool0_rotation': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'fan',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0, 1.0),
            (100.0, 100.0, 10.0, 20.0, 359.0),
            (0.0, 0.0, 50.0, 60.0, 359.0),
            (100.0, 100.0, 10.0, 20.0, 1.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0, 1.0),
            (100.0, 0.0, 50.0, 10.0, 359.0),
            (0.0, 100.0, 10.0, 50.0, 359.0),
            (100.0, 0.0, 50.0, 10.0, 1.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_fan_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_fan_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_fan_radius': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_fan_spread': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_fan_rotation': [1.0, 359.0, 359.0, 1.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_radius': [50.0, 10.0],
        'T0_tool0_clusters_spread': [60.0, 20.0],
        'T0_tool0_clusters_rotation': [0.0, 0.0],
        'T0_tool1_fan_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_fan_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_fan_radius': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_fan_spread': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_fan_rotation': [1.0, 359.0, 359.0, 1.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_radius': [10.0, 50.0],
        'T0_tool1_clusters_spread': [50.0, 10.0],
        'T0_tool1_clusters_rotation': [0.0, 0.0]
    },
    'frame1': {
        'T0_tool0_fan_x': [20.0],
        'T0_tool0_fan_y': [20.0],
        'T0_tool0_fan_radius': [20.0],
        'T0_tool0_fan_spread': [20.0],
        'T0_tool0_fan_rotation': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_fan_x': [50.0, 50.0],
        'T0_tool1_fan_y': [50.0, 50.0],
        'T0_tool1_fan_radius': [50.0, 50.0],
        'T0_tool1_fan_spread': [50.0, 50.0],
        'T0_tool1_fan_rotation': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_radius': [50.0],
        'T0_tool1_clusters_spread': [50.0],
        'T0_tool1_clusters_rotation': [50.0]
    }
}

TestShapeReducerFan = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape fan reducer with DBSCAN',
    pkwargs={'shape': 'fan'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [0.9868693567140278, 0.9868693567140278]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [0.9868693567140278, 0.9868693567140278]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1.0]

TestShapeReducerRotateRectangleHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape fan reducer with HDBSCAN',
    pkwargs={'shape': 'fan'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    }
)
