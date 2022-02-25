from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_width': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_width': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_width': [0.0, 100.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_width': [100.0, 0.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_width': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_width': [100.0, 0.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_width': [20.0]
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
    'shape': 'column',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0),
            (100.0, 100.0),
            (0.0, 0.0),
            (100.0, 100.0)
        ],
        'T0_tool1': [
            (0.0, 100.0),
            (100.0, 0.0),
            (0.0, 100.0),
            (100.0, 0.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0),
            (50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_column_width': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_width': [0.0, 100.0],
        'T0_tool1_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_column_width': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_width': [100.0, 0.0]
    },
    'frame1': {
        'T0_tool0_column_x': [20.0],
        'T0_tool0_column_width': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_column_x': [50.0, 50.0],
        'T0_tool1_column_width': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_width': [50.0]
    }
}

TestShapeReducerColumn = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape column reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerColumn'
)

TestShapeReducerColumnOptics = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape column reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerColumnOptics'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1.0]

TestShapeReducerColumnHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape column reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerColumnHdbscan'
)
