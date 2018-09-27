from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_rx': [50.0, 10.0],
            'T0_tool0_ry': [60.0, 20.0],
            'T0_tool0_angle': [179.0, -179.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_rx': [50.0],
            'T0_tool1_ry': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_rx': [50.0, 10.0],
            'T0_tool0_ry': [60.0, 20.0],
            'T0_tool0_angle': [-179.0, 179.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_rx': [10.0, 50.0],
            'T0_tool1_ry': [50.0, 10.0],
            'T0_tool1_angle': [179.0, -179.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_rx': [50.0],
            'T0_tool1_ry': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_rx': [10.0, 50.0],
            'T0_tool1_ry': [50.0, 10.0],
            'T0_tool1_angle': [-179.0, 179.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_rx': [20.0],
            'T0_tool0_ry': [20.0],
            'T0_tool0_angle': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'ellipse',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0, 179.0),
            (100.0, 100.0, 10.0, 20.0, -179.0),
            (0.0, 0.0, 50.0, 60.0, -179.0),
            (100.0, 100.0, 10.0, 20.0, 179.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0, 179.0),
            (100.0, 0.0, 50.0, 10.0, -179.0),
            (0.0, 100.0, 10.0, 50.0, -179.0),
            (100.0, 0.0, 50.0, 10.0, 179.0)
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
        'T0_tool0_ellipse_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_ellipse_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_ellipse_rx': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_ellipse_ry': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_ellipse_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_rx': [50.0, 10.0],
        'T0_tool0_clusters_ry': [60.0, 20.0],
        'T0_tool0_clusters_angle': [180.0, 180.0],
        'T0_tool1_ellipse_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_ellipse_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_ellipse_rx': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_ellipse_ry': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_ellipse_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_rx': [10.0, 50.0],
        'T0_tool1_clusters_ry': [50.0, 10.0],
        'T0_tool1_clusters_angle': [180.0, 180.0]
    },
    'frame1': {
        'T0_tool0_ellipse_x': [20.0],
        'T0_tool0_ellipse_y': [20.0],
        'T0_tool0_ellipse_rx': [20.0],
        'T0_tool0_ellipse_ry': [20.0],
        'T0_tool0_ellipse_angle': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_ellipse_x': [50.0, 50.0],
        'T0_tool1_ellipse_y': [50.0, 50.0],
        'T0_tool1_ellipse_rx': [50.0, 50.0],
        'T0_tool1_ellipse_ry': [50.0, 50.0],
        'T0_tool1_ellipse_angle': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_rx': [50.0],
        'T0_tool1_clusters_ry': [50.0],
        'T0_tool1_clusters_angle': [50.0]
    }
}

TestShapeReducerEllipse = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape ellipse reducer with DBSCAN',
    pkwargs={'shape': 'ellipse'},
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
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1.0]

TestShapeReducerEllipseHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape ellipse reducer with HDBSCAN',
    pkwargs={'shape': 'ellipse'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    }
)
