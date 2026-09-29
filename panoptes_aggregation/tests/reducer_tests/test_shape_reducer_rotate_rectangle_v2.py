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
            'T0_toolIndex0_width': [50.0, 10.0],
            'T0_toolIndex0_height': [60.0, 20.0],
            'T0_toolIndex0_angle': [179.0, -179.0]
        },
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_width': [50.0],
            'T0_toolIndex1_height': [50.0],
            'T0_toolIndex1_angle': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_width': [50.0, 10.0],
            'T0_toolIndex0_height': [60.0, 20.0],
            'T0_toolIndex0_angle': [-179.0, 179.0],
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_width': [10.0, 50.0],
            'T0_toolIndex1_height': [50.0, 10.0],
            'T0_toolIndex1_angle': [179.0, -179.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_width': [50.0],
            'T0_toolIndex1_height': [50.0],
            'T0_toolIndex1_angle': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_width': [10.0, 50.0],
            'T0_toolIndex1_height': [50.0, 10.0],
            'T0_toolIndex1_angle': [-179.0, 179.0]
        },
        'frame1': {
            'T0_toolIndex0_x_center': [20.0],
            'T0_toolIndex0_y_center': [20.0],
            'T0_toolIndex0_width': [20.0],
            'T0_toolIndex0_height': [20.0],
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
    'shape': 'rotateRectangle',
    'symmetric': False,
    'classifier_version': '2.0',
    'n_classifications': 5,
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
        'T0_toolIndex0_rotateRectangle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_rotateRectangle_y_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_rotateRectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex0_rotateRectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_toolIndex0_rotateRectangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_y_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_width': [50.0, 10.0],
        'T0_toolIndex0_clusters_height': [60.0, 20.0],
        'T0_toolIndex0_clusters_angle': [180.0, 180.0],
        'T0_toolIndex1_rotateRectangle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_rotateRectangle_y_center': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_rotateRectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_toolIndex1_rotateRectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex1_rotateRectangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex1_clusters_y_center': [100.0, 0.0],
        'T0_toolIndex1_clusters_width': [10.0, 50.0],
        'T0_toolIndex1_clusters_height': [50.0, 10.0],
        'T0_toolIndex1_clusters_angle': [180.0, 180.0]
    },
    'frame1': {
        'T0_toolIndex0_rotateRectangle_x_center': [20.0],
        'T0_toolIndex0_rotateRectangle_y_center': [20.0],
        'T0_toolIndex0_rotateRectangle_width': [20.0],
        'T0_toolIndex0_rotateRectangle_height': [20.0],
        'T0_toolIndex0_rotateRectangle_angle': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_rotateRectangle_x_center': [50.0, 50.0],
        'T0_toolIndex1_rotateRectangle_y_center': [50.0, 50.0],
        'T0_toolIndex1_rotateRectangle_width': [50.0, 50.0],
        'T0_toolIndex1_rotateRectangle_height': [50.0, 50.0],
        'T0_toolIndex1_rotateRectangle_angle': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x_center': [50.0],
        'T0_toolIndex1_clusters_y_center': [50.0],
        'T0_toolIndex1_clusters_width': [50.0],
        'T0_toolIndex1_clusters_height': [50.0],
        'T0_toolIndex1_clusters_angle': [50.0]
    }
}

TestShapeReducerRotateRectangle_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rotateRectangle V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerRotateRectangle_v2'
)

TestShapeReducerRotateRectangleOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rotateRectangle V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerRotateRectangleOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRotateRectangleHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape rotateRectangle V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRotateRectangleHdbscan_v2'
)

data_collab = [
    {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 0,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex0_0',
        'toolType': 'rotateRectangle',
        'x_center': 0.0,
        'y_center': 0.0,
        'width': 50.0,
        'height': 60.0,
        'angle': 180.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 0,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex0_1',
        'toolType': 'rotateRectangle',
        'x_center': 100.0,
        'y_center': 100.0,
        'width': 10.0,
        'height': 20.0,
        'angle': 180.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_0',
        'toolType': 'rotateRectangle',
        'x_center': 0.0,
        'y_center': 100.0,
        'width': 10.0,
        'height': 50.0,
        'angle': 180.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_1',
        'toolType': 'rotateRectangle',
        'x_center': 100.0,
        'y_center': 0.0,
        'width': 50.0,
        'height': 10.0,
        'angle': 180.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 1,
        'markId': 'collab_frame1_T0_toolIndex1_0',
        'toolType': 'rotateRectangle',
        'x_center': 50.0,
        'y_center': 50.0,
        'width': 50.0,
        'height': 50.0,
        'angle': 50.0
    }
]

reduced_data_collab = copy.deepcopy(reduced_data)
reduced_data_collab['data'] = data_collab
reduced_data_hdbscan_collab = copy.deepcopy(reduced_data_hdbscan)
reduced_data_hdbscan_collab['data'] = data_collab

TestShapeReducerRotateRectangle_v2_collab = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape rotateRectangle V2.0 reducer with DBSCAN with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRotateRectangle_v2_collab'
)

TestShapeReducerRotateRectangleOptics_v2_collab = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape rotateRectangle V2.0 reducer with OPTICS with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRotateRectangleOptics_v2_collab'
)

TestShapeReducerRotateRectangleHdbscan_v2_collab = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan_collab,
    'Test shape rotateRectangle V2.0 reducer with HDBSCAN with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True,
        'collab': True
    },
    test_name='TestShapeReducerRotateRectangleHdbscan_v2_collab'
)
