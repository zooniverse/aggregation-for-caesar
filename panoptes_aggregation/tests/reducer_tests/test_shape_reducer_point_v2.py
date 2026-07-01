from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x': [0.0, 100.0],
            'T0_toolIndex0_y': [0.0, 100.0]
        },
        'frame1': {
            'T0_toolIndex1_x': [50.0],
            'T0_toolIndex1_y': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x': [0.0, 100.0],
            'T0_toolIndex0_y': [0.0, 100.0],
            'T0_toolIndex1_x': [0.0, 100.0],
            'T0_toolIndex1_y': [100.0, 0.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x': [50.0],
            'T0_toolIndex1_y': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x': [0.0, 100.0],
            'T0_toolIndex1_y': [100.0, 0.0]
        },
        'frame1': {
            'T0_toolIndex0_x': [20.0],
            'T0_toolIndex0_y': [20.0]
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
    'shape': 'point',
    'symmetric': False,
    'classifier_version': '2.0',
    'n_classifications': 5,
    'frame0': {
        'T0_toolIndex0': [
            (0.0, 0.0),
            (100.0, 100.0),
            (0.0, 0.0),
            (100.0, 100.0)
        ],
        'T0_toolIndex1': [
            (0.0, 100.0),
            (100.0, 0.0),
            (0.0, 100.0),
            (100.0, 0.0)
        ]
    },
    'frame1': {
        'T0_toolIndex0': [
            (20.0, 20.0)
        ],
        'T0_toolIndex1': [
            (50.0, 50.0),
            (50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_toolIndex0_point_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_point_y': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x': [0.0, 100.0],
        'T0_toolIndex0_clusters_y': [0.0, 100.0],
        'T0_toolIndex1_point_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_point_y': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x': [0.0, 100.0],
        'T0_toolIndex1_clusters_y': [100.0, 0.0]
    },
    'frame1': {
        'T0_toolIndex0_point_x': [20.0],
        'T0_toolIndex0_point_y': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_point_x': [50.0, 50.0],
        'T0_toolIndex1_point_y': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x': [50.0],
        'T0_toolIndex1_clusters_y': [50.0]
    }
}

TestShapeReducerPoint_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape point V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerPoint_v2'
)

TestShapeReducerPointOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape point V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerPointOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerPointHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape point V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerPointHdbscan_v2'
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
        'toolType': 'point',
        'x': 0.0,
        'y': 0.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 0,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex0_1',
        'toolType': 'point',
        'x': 100.0,
        'y': 100.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_0',
        'toolType': 'point',
        'x': 0.0,
        'y': 100.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 0,
        'markId': 'collab_frame0_T0_toolIndex1_1',
        'toolType': 'point',
        'x': 100.0,
        'y': 0.0
    }, {
        'stepKey': 'S0',
        'taskIndex': 0,
        'taskKey': 'T0',
        'taskType': 'drawing',
        'toolIndex': 1,
        'frame': 1,
        'markId': 'collab_frame1_T0_toolIndex1_0',
        'toolType': 'point',
        'x': 50.0,
        'y': 50.0
    }
]

reduced_data_collab = copy.deepcopy(reduced_data)
reduced_data_collab['data'] = data_collab
reduced_data_hdbscan_collab = copy.deepcopy(reduced_data_hdbscan)
reduced_data_hdbscan_collab['data'] = data_collab

TestShapeReducerPoint_v2_collab = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape point V2.0 reducer with DBSCAN with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerPoint_v2_collab'
)

TestShapeReducerPointOptics_v2_collab = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_collab,
    'Test shape point V2.0 reducer with OPTICS with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerPointOptics_v2_collab'
)

TestShapeReducerPointHdbscan_v2_collab = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan_collab,
    'Test shape point V2.0 reducer with HDBSCAN with collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'point'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True,
        'collab': True
    },
    test_name='TestShapeReducerPointHdbscan_v2_collab'
)
