from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from .base_test_class import ReducerTest
import copy

# specific collab wrapper tests, use circle as example
# the same wrapper applies to all shapes, no need to test
# these parts elsewhere

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

data_collab_s1_t1 = [
    {
        'stepKey': 'S1',
        'taskIndex': 1,
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
        'stepKey': 'S1',
        'taskIndex': 1,
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
        'stepKey': 'S1',
        'taskIndex': 1,
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
        'stepKey': 'S1',
        'taskIndex': 1,
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
        'stepKey': 'S1',
        'taskIndex': 1,
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

reduced_data_collab_s1_t1 = copy.deepcopy(reduced_data)
reduced_data_collab_s1_t1['data'] = data_collab_s1_t1

TestShapeReducerCircle_v2_colab_2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab_s1_t1,
    'Test shape circle V2.0 reducer with DBSCAN and non default collab',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True,
        'step_key': 'S1',
        'task_index': 1
    },
    test_name='TestShapeReducerCircle_v2_collab_2'
)

reduced_data_collab_threshold = copy.deepcopy(reduced_data)
reduced_data_collab_threshold['data'] = []

TestShapeReducerCircle_v2_colab_3 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab_threshold,
    'Test shape circle V2.0 reducer with DBSCAN and high collab threshold',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'circle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True,
        'min_threshold': 0.5
    },
    test_name='TestShapeReducerCircle_v2_collab_3'
)
