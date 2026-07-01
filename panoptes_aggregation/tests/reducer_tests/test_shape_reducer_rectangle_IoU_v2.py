from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest
import copy


extracted_data = [
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [1.0],
            'T0_toolIndex0_y_center': [0.0],
            'T0_toolIndex0_width': [2.0],
            'T0_toolIndex0_height': [2.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [0.0],
            'T0_toolIndex0_y_center': [1.0],
            'T0_toolIndex0_width': [2.0],
            'T0_toolIndex0_height': [2.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [2.0],
            'T0_toolIndex0_y_center': [1.0],
            'T0_toolIndex0_width': [2.0],
            'T0_toolIndex0_height': [2.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x_center': [1.0],
            'T0_toolIndex0_y_center': [2.0],
            'T0_toolIndex0_width': [2.0],
            'T0_toolIndex0_height': [2.0]
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
    'n_classifications': 5,
    'frame0': {
        'T0_toolIndex0': [
            (1.0, 0.0, 2.0, 2.0),
            (0.0, 1.0, 2.0, 2.0),
            (2.0, 1.0, 2.0, 2.0),
            (1.0, 2.0, 2.0, 2.0)
        ],
    }
}

reduced_data = {
    'frame0': {
        'T0_toolIndex0_rectangle_x_center': [1.0, 0.0, 2.0, 1.0],
        'T0_toolIndex0_rectangle_y_center': [0.0, 1.0, 1.0, 2.0],
        'T0_toolIndex0_rectangle_width': [2.0, 2.0, 2.0, 2.0],
        'T0_toolIndex0_rectangle_height': [2.0, 2.0, 2.0, 2.0],
        'T0_toolIndex0_cluster_labels': [0, 0, 0, 0],
        'T0_toolIndex0_clusters_count': [4],
        'T0_toolIndex0_clusters_x_center': [1.0],
        'T0_toolIndex0_clusters_y_center': [1.0],
        'T0_toolIndex0_clusters_width': [2.0],
        'T0_toolIndex0_clusters_height': [2.0],
        'T0_toolIndex0_clusters_sigma': [0.8],
    }
}

TestShapeReducerRectangleIoU_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle V2.0 reducer with DBSCAN and IoU metric',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 0.9,
        'min_samples': 2,
        'metric_type': 'IoU'
    },
    test_name='TestShapeReducerRectangleIoU_v2',
    round=1
)

TestShapeReducerRectangleIoUOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle V2.0 reducer with OPTICS and IoU metric',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2,
        'metric_type': 'IoU'
    },
    test_name='TestShapeReducerRectangleIoUOptics_v2',
    round=1
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]

TestShapeReducerRectangleIoUHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape rectangle V2.0 reducer with HDBSCAN and IoU metric',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2,
        'min_cluster_size': 2,
        'metric_type': 'IoU',
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleIoUHdbscan_v2',
    round=1
)
