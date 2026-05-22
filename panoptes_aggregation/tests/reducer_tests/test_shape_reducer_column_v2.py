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
            'T0_toolIndex0_width': [0.0, 100.0]
        },
        'frame1': {
            'T0_toolIndex1_x': [50.0],
            'T0_toolIndex1_width': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex0_x': [0.0, 100.0],
            'T0_toolIndex0_width': [0.0, 100.0],
            'T0_toolIndex1_x': [0.0, 100.0],
            'T0_toolIndex1_width': [100.0, 0.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame1': {
            'T0_toolIndex1_x': [50.0],
            'T0_toolIndex1_width': [50.0]
        }
    },
    {
        'classifier_version': '2.0',
        'frame0': {
            'T0_toolIndex1_x': [0.0, 100.0],
            'T0_toolIndex1_width': [100.0, 0.0]
        },
        'frame1': {
            'T0_toolIndex0_x': [20.0],
            'T0_toolIndex0_width': [20.0]
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
    'classifier_version': '2.0',
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

processed_data_graph2dRangeX = copy.deepcopy(processed_data)
processed_data_graph2dRangeX['shape'] = 'graph2dRangeX'

reduced_data = {
    'frame0': {
        'T0_toolIndex0_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_column_width': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x': [0.0, 100.0],
        'T0_toolIndex0_clusters_width': [0.0, 100.0],
        'T0_toolIndex1_column_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_column_width': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x': [0.0, 100.0],
        'T0_toolIndex1_clusters_width': [100.0, 0.0]
    },
    'frame1': {
        'T0_toolIndex0_column_x': [20.0],
        'T0_toolIndex0_column_width': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_column_x': [50.0, 50.0],
        'T0_toolIndex1_column_width': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x': [50.0],
        'T0_toolIndex1_clusters_width': [50.0]
    }
}

reduced_data_graph2dRangeX = {
    'frame0': {
        'T0_toolIndex0_graph2dRangeX_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_graph2dRangeX_width': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex0_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex0_clusters_count': [2, 2],
        'T0_toolIndex0_clusters_x': [0.0, 100.0],
        'T0_toolIndex0_clusters_width': [0.0, 100.0],
        'T0_toolIndex1_graph2dRangeX_x': [0.0, 100.0, 0.0, 100.0],
        'T0_toolIndex1_graph2dRangeX_width': [100.0, 0.0, 100.0, 0.0],
        'T0_toolIndex1_cluster_labels': [0, 1, 0, 1],
        'T0_toolIndex1_clusters_count': [2, 2],
        'T0_toolIndex1_clusters_x': [0.0, 100.0],
        'T0_toolIndex1_clusters_width': [100.0, 0.0]
    },
    'frame1': {
        'T0_toolIndex0_graph2dRangeX_x': [20.0],
        'T0_toolIndex0_graph2dRangeX_width': [20.0],
        'T0_toolIndex0_cluster_labels': [-1],
        'T0_toolIndex1_graph2dRangeX_x': [50.0, 50.0],
        'T0_toolIndex1_graph2dRangeX_width': [50.0, 50.0],
        'T0_toolIndex1_cluster_labels': [0, 0],
        'T0_toolIndex1_clusters_count': [2],
        'T0_toolIndex1_clusters_x': [50.0],
        'T0_toolIndex1_clusters_width': [50.0]
    }
}

TestShapeReducerColumn_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape column V2.0 reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerColumn_v2'
)

TestShapeReducerGraph2dRangeX_v2 = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data_graph2dRangeX,
    reduced_data_graph2dRangeX,
    'Test shape graph2dRangeX reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'graph2dRangeX'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerGraph2dRangeX_v2'
)

TestShapeReducerColumnOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape column V2.0 reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerColumnOptics_v2'
)

TestShapeReducerGraph2dRangeXOptics_v2 = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data_graph2dRangeX,
    reduced_data_graph2dRangeX,
    'Test shape graph2dRangeX reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'graph2dRangeX'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerGraph2dRangeXOptics_v2'
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]

reduced_data_hdbscan_graph2dRangeX = copy.deepcopy(reduced_data_graph2dRangeX)
reduced_data_hdbscan_graph2dRangeX['frame0']['T0_toolIndex0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_graph2dRangeX['frame0']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_graph2dRangeX['frame1']['T0_toolIndex0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_graph2dRangeX['frame1']['T0_toolIndex1_cluster_probabilities'] = [1.0, 1.0]


TestShapeReducerColumnHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape column V2.0 reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'column'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerColumnHdbscan_v2'
)

TestShapeReducerGraph2dRangeXHdbscan_v2 = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data_graph2dRangeX,
    reduced_data_hdbscan_graph2dRangeX,
    'Test shape graph2dRangeX reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'graph2dRangeX'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerGraph2dRangeXHdbscan_v2'
)
