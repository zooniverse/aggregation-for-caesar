from panoptes_aggregation.reducers.shape_reducer_dbscan import shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import shape_reducer_optics
from .base_test_class import ReducerTestNoProcessing
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_y': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool1_y': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool1_y': [0.0, 100.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_y': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_y': [0.0, 100.0]
        },
        'frame1': {
            'T0_tool0_y': [20.0]
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
    'shape': 'fullWidthLine',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0),
            (100.0),
            (0.0),
            (100.0)
        ],
        'T0_tool1': [
            (0.0),
            (100.0),
            (0.0),
            (100.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0)
        ],
        'T0_tool1': [
            (50.0),
            (50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_fullWidthLine_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool1_fullWidthLine_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_y': [0.0, 100.0]
    },
    'frame1': {
        'T0_tool0_fullWidthLine_y': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_fullWidthLine_y': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_y': [50.0]
    }
}

TestShapeReducerFullWidthLine = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data,
    'Test shape fullWidthLine reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'shape': 'fullWidthLine'
    },
    test_name='TestShapeReducerFullWidthLine'
)

TestShapeReducerFullWidthLineOptics = ReducerTestNoProcessing(
    shape_reducer_optics,
    extracted_data,
    reduced_data,
    'Test shape fullWidthLine reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_samples': 2,
        'shape': 'fullWidthLine'
    },
    test_name='TestShapeReducerFullWidthLineOptics'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1, 1, 1, 1]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [1, 1]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1, 1, 1, 1]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [1, 1]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1, 1]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1]

TestShapeReducerFullWidthLineHdbscan = ReducerTestNoProcessing(
    shape_reducer_hdbscan,
    extracted_data,
    reduced_data_hdbscan,
    'Test shape fullWidthLine reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True,
        'shape': 'fullWidthLine'
    },
    test_name='TestShapeReducerFullWidthLineHdbscan'
)
