from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest, ReducerTestNoProcessing
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [60.0, 20.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [60.0, 20.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [50.0, 10.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [50.0, 10.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_width': [20.0],
            'T0_tool0_height': [20.0]
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
    'n_classifications': 5,
    'shape': 'rectangle',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0),
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0),
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [60.0, 20.0],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [50.0, 10.0],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangle = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangle'
)

TestShapeReducerRectangleOptics = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangleOptics'
)


reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape rectangle reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleHdbscan'
)


reduced_data_collab_true = {
'data': [
        {
            "frame": 0,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 0,
            "toolType": "freehandLine",
            "rec_x": 0.0,
            "rec_y": 0.0,
            "rec_width": 50.0,
            "rec_height": 60.0
        },
{
            "frame": 0,
            "markID": "consensus_1",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 0,
            "toolType": "freehandLine",
            "rec_x": 100.0,
            "rec_y": 100.0,
            "rec_width": 10.0,
            "rec_height": 20.0
        },
        {
            "frame": 0,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "rec_x": 0.0,
            "rec_y": 100.0,
            "rec_width": 10.0,
            "rec_height": 50.0,
        },
{
            "frame": 0,
            "markID": "consensus_1",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "rec_x": 100.0,
            "rec_y": 0.0,
            "rec_width": 50.0,
            "rec_height": 10.0
        },
{
            "frame": 1,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "rec_x": 50.0,
            "rec_y": 50.0,
            "rec_width": 50.0,
            "rec_height": 50.0
        }
        ],
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [60.0, 20.0],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [50.0, 10.0],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangleDbscanCollabTrue = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab_true,
    'Test shape rectangle reducer with DBSCAN when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRectangleDBScanCollabTrue'
)

TestShapeReducerRectangleOpticsCollabTrue = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_collab_true,
    'Test shape rectangle reducer with OPTICS when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRectangleOpticsCollabTrue'
)

reduced_data_hdbscan_collab_true = copy.deepcopy(reduced_data_collab_true)
reduced_data_hdbscan_collab_true['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_collab_true['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_collab_true['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_collab_true['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscanCollabTrue = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan_collab_true,
    'Test shape rectangle reducer with HDBSCAN when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'collab': True,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleHdbscanCollabTrue'
)

reduced_data_min_threshold = {
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [],
        'T0_tool0_clusters_y': [],
        'T0_tool0_clusters_width': [],
        'T0_tool0_clusters_height': [],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [],
        'T0_tool1_clusters_y': [],
        'T0_tool1_clusters_width': [],
        'T0_tool1_clusters_height': [],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [],
        'T0_tool1_clusters_y': [],
        'T0_tool1_clusters_width': [],
        'T0_tool1_clusters_height': [],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangleDbscanMinThreshold = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data_min_threshold,
    'Test shape rectangle reducer with DBSCAN when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True,
        'min_threshold': 0.5,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleDBScanMinThreshold'
)


TestShapeReducerRectangleOpticsMinThreshold = ReducerTestNoProcessing(
    shape_reducer_optics,
    extracted_data,
    reduced_data_min_threshold,
    'Test shape rectangle reducer with OPTICS when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_samples': 2,
        'collab': True,
        'min_threshold': 0.5,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleOpticsMinThreshold'
)

reduced_data_hdbscan_min_threshold = copy.deepcopy(reduced_data_min_threshold)
reduced_data_hdbscan_min_threshold['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_min_threshold['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_min_threshold['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_min_threshold['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscanMinThreshold = ReducerTestNoProcessing(
    shape_reducer_hdbscan,
    extracted_data,
    reduced_data_hdbscan_collab_true,
    'Test shape rectangle reducer with HDBSCAN when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'collab': True,
        'allow_single_cluster': True,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleHdbscanMinThreshold'
)