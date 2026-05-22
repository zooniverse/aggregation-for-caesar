from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_rx': [50.0, 10.0],
            'T0_toolIndex0_ry': [60.0, 20.0],
            'T0_toolIndex0_angle': [179.0, -179.0]
        },
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_rx': [50.0],
            'T0_toolIndex1_ry': [50.0],
            'T0_toolIndex1_angle': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_rx': [50.0, 10.0],
            'T0_toolIndex0_ry': [60.0, 20.0],
            'T0_toolIndex0_angle': [-179.0, 179.0],
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_rx': [10.0, 50.0],
            'T0_toolIndex1_ry': [50.0, 10.0],
            'T0_toolIndex1_angle': [179.0, -179.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_rx': [50.0],
            'T0_toolIndex1_ry': [50.0],
            'T0_toolIndex1_angle': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_rx': [10.0, 50.0],
            'T0_toolIndex1_ry': [50.0, 10.0],
            'T0_toolIndex1_angle': [-179.0, 179.0]
        },
        'frame1': {
            'T0_toolIndex0_x_center': [20.0],
            'T0_toolIndex0_y_center': [20.0],
            'T0_toolIndex0_rx': [20.0],
            'T0_toolIndex0_ry': [20.0],
            'T0_toolIndex0_angle': [20.0]
        }
    },
    {}
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        3,
        4,
        5
    ]
}

processed_data = {
    'shape': 'ellipse',
    'symmetric': False,
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0': [
            (0.0, 0.0, 50.0, 60.0, 179.0),
            (100.0, 100.0, 10.0, 20.0, -179.0),
            (0.0, 0.0, 50.0, 60.0, -179.0),
            (100.0, 100.0, 10.0, 20.0, 179.0)
        ],
        'T0_toolIndex1': [
            (0.0, 100.0, 10.0, 50.0, 179.0),
            (100.0, 0.0, 50.0, 10.0, -179.0),
            (0.0, 100.0, 10.0, 50.0, -179.0),
            (100.0, 0.0, 50.0, 10.0, 179.0)
        ]
    },
    'frame1': {
        'T0_toolIndex0': [
            (20.0, 20.0, 20.0, 20.0, 20.0)
        ],
        'T0_toolIndex1': [
            (50.0, 50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_toolIndex0_ellipse_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_ellipse_y_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_ellipse_rx': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex0_ellipse_ry': [60.0, 20.0, 60.0, 20.0],
        'T0_toolIndex0_ellipse_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_y_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_rx': [50.0, 10.0],
        'T0_toolIndex0_clusters_ry': [60.0, 20.0],
        'T0_toolIndex0_clusters_angle': [180.0, 180.0],
        'T0_toolIndex1_ellipse_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_ellipse_y_center': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_ellipse_rx': [10.0, 50.0, 10.0, 50.0],
        'T0_toolIndex1_ellipse_ry': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex1_ellipse_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex1_clusters_y_center': [100.0, 0.0],
        'T0_toolIndex1_clusters_rx': [10.0, 50.0],
        'T0_toolIndex1_clusters_ry': [50.0, 10.0],
        'T0_toolIndex1_clusters_angle': [180.0, 180.0]
    },
    'frame1': {
        'T0_toolIndex0_ellipse_x_center': [20.0],
        'T0_toolIndex0_ellipse_y_center': [20.0],
        'T0_toolIndex0_ellipse_rx': [20.0],
        'T0_toolIndex0_ellipse_ry': [20.0],
        'T0_toolIndex0_ellipse_angle': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_ellipse_x_center': [50.0, 50.0],
        'T0_toolIndex1_ellipse_y_center': [50.0, 50.0],
        'T0_toolIndex1_ellipse_rx': [50.0, 50.0],
        'T0_toolIndex1_ellipse_ry': [50.0, 50.0],
        'T0_toolIndex1_ellipse_angle': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x_center': [50.0],
        'T0_toolIndex1_clusters_y_center': [50.0],
        'T0_toolIndex1_clusters_rx': [50.0],
        'T0_toolIndex1_clusters_ry': [50.0],
        'T0_toolIndex1_clusters_angle': [50.0]
    }
}

TestShapeReducerEllipse_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape ellipse V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'ellipse'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerEllipse_v2'
)

TestShapeReducerEllipseOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape ellipse V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'ellipse'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerEllipseOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerEllipseHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape ellipse V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'ellipse'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerEllipseHdbscan_v2'
)
