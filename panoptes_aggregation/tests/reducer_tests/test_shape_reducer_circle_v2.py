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
            'T0_toolIndex0_r': [50.0, 10.0]
        },
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_r': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_r': [50.0, 10.0],
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_r': [10.0, 50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_r': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_r': [10.0, 50.0]
        },
        'frame1': {
            'T0_toolIndex0_x_center': [20.0],
            'T0_toolIndex0_y_center': [20.0],
            'T0_toolIndex0_r': [20.0]
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
    'shape': 'circle',
    'n_classifications': 5,
    'symmetric': False,
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0': [
            (0.0, 0.0, 50.0),
            (100.0, 100.0, 10.0),
            (0.0, 0.0, 50.00),
            (100.0, 100.0, 10.0)
        ],
        'T0_toolIndex1': [
            (0.0, 100.0, 10.0),
            (100.0, 0.0, 50.0),
            (0.0, 100.0, 10.0),
            (100.0, 0.0, 50.0)
        ]
    },
    'frame1': {
        'T0_toolIndex0': [
            (20.0, 20.0, 20.0)
        ],
        'T0_toolIndex1': [
            (50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_toolIndex0_circle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_circle_y_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_circle_r': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_y_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_r': [50.0, 10.0],
        'T0_toolIndex1_circle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_circle_y_center': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_circle_r': [10.0, 50.0, 10.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex1_clusters_y_center': [100.0, 0.0],
        'T0_toolIndex1_clusters_r': [10.0, 50.0]
    },
    'frame1': {
        'T0_toolIndex0_circle_x_center': [20.0],
        'T0_toolIndex0_circle_y_center': [20.0],
        'T0_toolIndex0_circle_r': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_circle_x_center': [50.0, 50.0],
        'T0_toolIndex1_circle_y_center': [50.0, 50.0],
        'T0_toolIndex1_circle_r': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x_center': [50.0],
        'T0_toolIndex1_clusters_y_center': [50.0],
        'T0_toolIndex1_clusters_r': [50.0]
    }
}

TestShapeReducerCircle_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape circle V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerCircle_v2'
)

TestShapeReducerCircleOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape circle V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerCircleOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerCircleHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape circle V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerCircleHdbscan_v2'
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
        'toolType': 'circle',
        'x_center': 0.0,
        'y_center': 0.0,
        'r': 50.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 0,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex0_1',
        'toolType': 'circle',
        'x_center': 100.0,
        'y_center': 100.0,
        'r': 10.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_0',
        'toolType': 'circle',
        'x_center': 0.0,
        'y_center': 100.0,
        'r': 10.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_1',
        'toolType': 'circle',
        'x_center': 100.0,
        'y_center': 0.0,
        'r': 50.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 1,
        'markId': 'collab_frame1_T0_toolIndex1_0',
        'toolType': 'circle',
        'x_center': 50.0,
        'y_center': 50.0,
        'r': 50.0
    }
]

reduced_data_collab = copy.deepcopy(reduced_data)
reduced_data_collab['data'] = data_collab
reduced_data_hdbscan_collab = copy.deepcopy(reduced_data_hdbscan)
reduced_data_hdbscan_collab['data'] = data_collab

TestShapeReducerCircle_v2_colab = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape circle V2.0 reducer with DBSCAN and collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerCircle_v2_collab'
)

TestShapeReducerCircleOptics_v2_collab = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape circle V2.0 reducer with OPTICS and collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerCircleOptics_v2_collab'
)

TestShapeReducerCircleHdbscan_v2_collab = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan_collab,
    'Test shape circle V2.0 reducer with HDBSCAN and collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True,
        'collab': True
    },
    test_name='TestShapeReducerCircleHdbscan_v2_collab'
)
