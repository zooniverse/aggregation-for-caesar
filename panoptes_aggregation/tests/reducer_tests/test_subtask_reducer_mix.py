from panoptes_aggregation.reducers.shape_reducer_dbscan import shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import shape_reducer_optics
from .base_test_class import ReducerTestNoProcessing
import copy


extracted_data = [{
    "frame0": {
        "T0_tool0_x": [0.0, 100.0],
        "T0_tool0_y": [0.0, 105.0],
        "T0_tool0_width": [5.0, 50.0],
        "T0_tool0_height": [10.0, 100.0],
        "T0_tool0_details": [
            [{"0": 1}, {"1": 1}],
            [{"1": 1}, {"2": 1}]
        ],
        "T0_tool1_x": [500.0],
        "T0_tool1_y": [500.0],
        "T0_tool1_width": [10.0],
        "T0_tool1_height": [20.0]
    }
}, {
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_x_center": [2.5, 125.0],
        "T0_toolIndex0_y_center": [5.0, 155.0],
        "T0_toolIndex0_width": [5.0, 50.0],
        "T0_toolIndex0_height": [10.0, 100.0],
        "T0_toolIndex0_subtask0": [{"1": 1}, {"0": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
    }
}]

kwargs_extra_data = {
    'user_id': [
        1,
        2
    ]
}

reduced_data = {
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125, 2.5, 125],
        "T0_toolIndex0_rectangle_y_center": [5.0, 155.0, 5.0, 155.0],
        "T0_toolIndex0_rectangle_width": [5.0, 50.0, 5.0, 50.0],
        "T0_toolIndex0_rectangle_height": [10.0, 100.0, 10.0, 100.0],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_subtask0": [
            {"0": 1},
            {"1": 1},
            {"1": 1},
            {"0": 1},
        ],
        "T0_toolIndex0_subtask1": [
            {"1": 1},
            {"2": 1},
            {"1": 1},
            {"2": 1}
        ],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125.0],
        "T0_toolIndex0_clusters_y_center": [5.0, 155.0],
        "T0_toolIndex0_clusters_width": [5.0, 50.0],
        "T0_toolIndex0_clusters_height": [10.0, 100.0],

        "T0_toolIndex0_subtask0_clusters": [
            {"0": 1, "1": 1},
            {"0": 1, "1": 1}
        ],
        "T0_toolIndex0_subtask1_clusters": [
            {"1": 2},
            {"2": 2}
        ],

        "T0_toolIndex1_rectangle_x_center": [505.0],
        "T0_toolIndex1_rectangle_y_center": [510.0],
        "T0_toolIndex1_rectangle_width": [10.0],
        "T0_toolIndex1_rectangle_height": [20.0],
        "T0_toolIndex1_cluster_labels": [-1],
    }
}

TestSubtaskReducerMixDBSCAN = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test subtask reducer with mixed classifier versions with DBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_toolIndex0_subtask0': 'question_reducer',
            'T0_toolIndex0_subtask1': 'question_reducer'
        }
    },
    test_name='TestSubtaskReducerMixDBSCAN'
)

TestSubtaskReducerMixOptics = ReducerTestNoProcessing(
    shape_reducer_optics,
    extracted_data,
    reduced_data,
    'Test subtask reducer with mixed classifier versions with OPTICS',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'min_samples': 2,
        'details': {
            'T0_toolIndex0_subtask0': 'question_reducer',
            'T0_toolIndex0_subtask1': 'question_reducer'
        }
    },
    test_name='TestSubtaskReducerMixOptics'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [0]

TestSubtaskReducerMixHDBSCAN = ReducerTestNoProcessing(
    shape_reducer_hdbscan,
    extracted_data,
    reduced_data_hdbscan,
    'Test subtask reducer with mixed classifier versions with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'min_cluster_size': 2,
        'min_samples': 2,
        'details': {
            'T0_toolIndex0_subtask0': 'question_reducer',
            'T0_toolIndex0_subtask1': 'question_reducer'
        }
    },
    test_name='TestSubtaskReducerMixHDBSCAN'
)

TestSubtaskReducerMixV1Config = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test subtask reducer with mixed classifier versions and v1.0 details config',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_tool0': ['question_reducer', 'question_reducer']
        }
    },
    test_name='TestSubtaskReducerMixV1Config'
)

reduced_data_no_details = {
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125.0, 2.5, 125.0],
        "T0_toolIndex0_rectangle_y_center": [5.0, 155.0, 5.0, 155.0],
        "T0_toolIndex0_rectangle_width": [5.0, 50.0, 5.0, 50.0],
        "T0_toolIndex0_rectangle_height": [10.0, 100.0, 10.0, 100.0],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125.0],
        "T0_toolIndex0_clusters_y_center": [5.0, 155.0],
        "T0_toolIndex0_clusters_width": [5.0, 50.0],
        "T0_toolIndex0_clusters_height": [10.0, 100.0],

        "T0_toolIndex1_rectangle_x_center": [505.0],
        "T0_toolIndex1_rectangle_y_center": [510.0],
        "T0_toolIndex1_rectangle_width": [10.0],
        "T0_toolIndex1_rectangle_height": [20.0],
        "T0_toolIndex1_cluster_labels": [-1],
    }
}

TestSubtaskReducerMixNoDetails = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data_no_details,
    'Test subtask reducer with mixed classifier versions with no details',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'shape': 'rectangle',
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestSubtaskReducerMixNoDetails'
)
