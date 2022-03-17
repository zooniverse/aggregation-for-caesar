from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x1': [0.0, 100.0],
            'T0_tool0_y1': [0.0, 100.0],
            'T0_tool0_x2': [50.0, 10.0],
            'T0_tool0_y2': [60.0, 20.0]
        },
        'frame1': {
            'T0_tool1_x1': [70.0],
            'T0_tool1_y1': [70.0],
            'T0_tool1_x2': [50.0],
            'T0_tool1_y2': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x1': [0.0, 100.0],
            'T0_tool0_y1': [0.0, 100.0],
            'T0_tool0_x2': [50.0, 10.0],
            'T0_tool0_y2': [60.0, 20.0],
            'T0_tool1_x1': [0.0, 100.0],
            'T0_tool1_y1': [100.0, 0.0],
            'T0_tool1_x2': [10.0, 50.0],
            'T0_tool1_y2': [50.0, 10.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x1': [50.0],
            'T0_tool1_y1': [50.0],
            'T0_tool1_x2': [70.0],
            'T0_tool1_y2': [70.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x1': [0.0, 100.0],
            'T0_tool1_y1': [100.0, 0.0],
            'T0_tool1_x2': [10.0, 50.0],
            'T0_tool1_y2': [50.0, 10.0]
        },
        'frame1': {
            'T0_tool0_x1': [20.0],
            'T0_tool0_y1': [20.0],
            'T0_tool0_x2': [20.0],
            'T0_tool0_y2': [20.0]
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
    'shape': 'line',
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
            (70.0, 70.0, 50.0, 50.0),
            (50.0, 50.0, 70.0, 70.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_line_x1': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_line_y1': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_line_x2': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_line_y2': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x1': [0.0, 100.0],
        'T0_tool0_clusters_y1': [0.0, 100.0],
        'T0_tool0_clusters_x2': [50.0, 10.0],
        'T0_tool0_clusters_y2': [60.0, 20.0],
        'T0_tool1_line_x1': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_line_y1': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_line_x2': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_line_y2': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x1': [0.0, 100.0],
        'T0_tool1_clusters_y1': [100.0, 0.0],
        'T0_tool1_clusters_x2': [10.0, 50.0],
        'T0_tool1_clusters_y2': [50.0, 10.0]
    },
    'frame1': {
        'T0_tool0_line_x1': [20.0],
        'T0_tool0_line_y1': [20.0],
        'T0_tool0_line_x2': [20.0],
        'T0_tool0_line_y2': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_line_x1': [70.0, 50.0],
        'T0_tool1_line_y1': [70.0, 50.0],
        'T0_tool1_line_x2': [50.0, 70.0],
        'T0_tool1_line_y2': [50.0, 70.0],
        'T0_tool1_cluster_labels': [-1, -1]
    }
}


TestShapeReducerLine = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape line reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'line'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerLine'
)

reduced_data_optics = copy.deepcopy(reduced_data)
reduced_data_optics['frame1']['T0_tool1_cluster_labels'] = [0, 0]
reduced_data_optics['frame1']['T0_tool1_clusters_count'] = [2]
reduced_data_optics['frame1']['T0_tool1_clusters_x1'] = [60.0]
reduced_data_optics['frame1']['T0_tool1_clusters_x2'] = [60.0]
reduced_data_optics['frame1']['T0_tool1_clusters_y1'] = [60.0]
reduced_data_optics['frame1']['T0_tool1_clusters_y2'] = [60.0]

TestShapeReducerLineOptics = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_optics,
    'Test shape line reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'line'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerLineOptics'
)

processed_data_symmetric = {
    'shape': 'line',
    'symmetric': True,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0),
            (10.0, 20.0, 100.0, 100.0),
            (0.0, 0.0, 50.0, 60.0),
            (10.0, 20.0, 100.0, 100.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0),
            (50.0, 10.0, 100.0, 0.0),
            (0.0, 100.0, 10.0, 50.0),
            (50.0, 10.0, 100.0, 0.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 70.0, 70.0),
            (50.0, 50.0, 70.0, 70.0)
        ]
    }
}

reduced_data_symmetric = {
    'frame0': {
        'T0_tool0_line_x1': [0.0, 10.0, 0.0, 10.0],
        'T0_tool0_line_y1': [0.0, 20.0, 0.0, 20.0],
        'T0_tool0_line_x2': [50.0, 100.0, 50.0, 100.0],
        'T0_tool0_line_y2': [60.0, 100.0, 60.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x1': [0.0, 10.0],
        'T0_tool0_clusters_y1': [0.0, 20.0],
        'T0_tool0_clusters_x2': [50.0, 100.0],
        'T0_tool0_clusters_y2': [60.0, 100.0],
        'T0_tool1_line_x1': [0.0, 50.0, 0.0, 50.0],
        'T0_tool1_line_y1': [100.0, 10.0, 100.0, 10.0],
        'T0_tool1_line_x2': [10.0, 100.0, 10.0, 100.0],
        'T0_tool1_line_y2': [50.0, 0.0, 50.0, 0.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x1': [0.0, 50.0],
        'T0_tool1_clusters_y1': [100.0, 10.0],
        'T0_tool1_clusters_x2': [10.0, 100.0],
        'T0_tool1_clusters_y2': [50.0, 0.0]
    },
    'frame1': {
        'T0_tool0_line_x1': [20.0],
        'T0_tool0_line_y1': [20.0],
        'T0_tool0_line_x2': [20.0],
        'T0_tool0_line_y2': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_line_x1': [50.0, 50.0],
        'T0_tool1_line_y1': [50.0, 50.0],
        'T0_tool1_line_x2': [70.0, 70.0],
        'T0_tool1_line_y2': [70.0, 70.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x1': [50.0],
        'T0_tool1_clusters_y1': [50.0],
        'T0_tool1_clusters_x2': [70.0],
        'T0_tool1_clusters_y2': [70.0]
    }
}

TestShapeReducerLineSymmetric = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data_symmetric,
    reduced_data_symmetric,
    'Test shape line reducer with DBSCAN with symmetries',
    network_kwargs=kwargs_extra_data,
    pkwargs={
        'shape': 'line',
        'symmetric': True
    },
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerLineSymmetric'
)

TestShapeReducerLineSymmetricOptics = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data_symmetric,
    reduced_data_symmetric,
    'Test shape line reducer with OPTICS with symmetries',
    network_kwargs=kwargs_extra_data,
    pkwargs={
        'shape': 'line',
        'symmetric': True
    },
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerLineSymmetricOptics'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]

reduced_data_hdbscan['frame1']['T0_tool1_cluster_labels'] = [0, 0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_count'] = [2]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_x1'] = [60.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_y1'] = [60.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_x2'] = [60.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_y2'] = [60.0]

TestShapeReducerLineHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape line reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'line'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerLineHdbscan'
)

reduced_data_hdbscan_symmetric = copy.deepcopy(reduced_data_symmetric)
reduced_data_hdbscan_symmetric['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_symmetric['frame0']['T0_tool0_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan_symmetric['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_symmetric['frame0']['T0_tool1_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan_symmetric['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_symmetric['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan_symmetric['frame1']['T0_tool1_clusters_persistance'] = [1.0]

TestShapeReducerLineHdbscanSymmetric = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data_symmetric,
    reduced_data_hdbscan_symmetric,
    'Test shape line reducer with HDBSCAN with symmetries',
    network_kwargs=kwargs_extra_data,
    pkwargs={
        'shape': 'line',
        'symmetric': True
    },
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerLineHdbscanSymmetric'
)
