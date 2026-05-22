from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest, ReducerTestNoProcessing
import copy

extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_width': [50.0, 10.0],
            'T0_toolIndex0_height': [60.0, 20.0]
        },
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_width': [50.0],
            'T0_toolIndex1_height': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0, 100.0],
            'T0_toolIndex0_y_center': [0.0, 100.0],
            'T0_toolIndex0_width': [50.0, 10.0],
            'T0_toolIndex0_height': [60.0, 20.0],
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_width': [10.0, 50.0],
            'T0_toolIndex1_height': [50.0, 10.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x_center': [50.0],
            'T0_toolIndex1_y_center': [50.0],
            'T0_toolIndex1_width': [50.0],
            'T0_toolIndex1_height': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x_center': [0.0, 100.0],
            'T0_toolIndex1_y_center': [100.0, 0.0],
            'T0_toolIndex1_width': [10.0, 50.0],
            'T0_toolIndex1_height': [50.0, 10.0]
        },
        'frame1': {
            'T0_toolIndex0_x_center': [20.0],
            'T0_toolIndex0_y_center': [20.0],
            'T0_toolIndex0_width': [20.0],
            'T0_toolIndex0_height': [20.0]
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
    'shape': 'rectangle',
    'symmetric': False,
    'classifier_version': '2.0',
    'frame0': {
        'T0_toolIndex0': [
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0),
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0)
        ],
        'T0_toolIndex1': [
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0),
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0)
        ]
    },
    'frame1': {
        'T0_toolIndex0': [
            (20.0, 20.0, 20.0, 20.0)
        ],
        'T0_toolIndex1': [
            (50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_toolIndex0_rectangle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_rectangle_y_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_y_center': [0.0, 100.0],
        'T0_toolIndex0_clusters_width': [50.0, 10.0],
        'T0_toolIndex0_clusters_height': [60.0, 20.0],
        'T0_toolIndex1_rectangle_x_center': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_rectangle_y_center': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_toolIndex1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x_center': [0.0, 100.0],
        'T0_toolIndex1_clusters_y_center': [100.0, 0.0],
        'T0_toolIndex1_clusters_width': [10.0, 50.0],
        'T0_toolIndex1_clusters_height': [50.0, 10.0]
    },
    'frame1': {
        'T0_toolIndex0_rectangle_x_center': [20.0],
        'T0_toolIndex0_rectangle_y_center': [20.0],
        'T0_toolIndex0_rectangle_width': [20.0],
        'T0_toolIndex0_rectangle_height': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_rectangle_x_center': [50.0, 50.0],
        'T0_toolIndex1_rectangle_y_center': [50.0, 50.0],
        'T0_toolIndex1_rectangle_width': [50.0, 50.0],
        'T0_toolIndex1_rectangle_height': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x_center': [50.0],
        'T0_toolIndex1_clusters_y_center': [50.0],
        'T0_toolIndex1_clusters_width': [50.0],
        'T0_toolIndex1_clusters_height': [50.0]
    }
}

TestShapeReducerRectangle_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangle_v2'
)

TestShapeReducerRectangleOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangleOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape rectangle V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleHdbscan_v2'
)
