from panoptes_aggregation.reducers.point_process_data import process_temporal_data
from panoptes_aggregation.reducers.temporal_point_reducer_dbscan import temporal_point_reducer_dbscan
from panoptes_aggregation.reducers.temporal_point_reducer_hdbscan import temporal_point_reducer_hdbscan
from .base_test_class import ReducerTest

extracted_data = classifications = [
    {
        'aggregation_version': '4.0.0',
        'frame0': {
            'T0_toolIndex0_x': [2000],
            'T0_toolIndex0_displayTime': [0.],
            'T0_toolIndex0_y': [50],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [15],
            'T0_toolIndex0_displayTime': [0.1],
            'T0_toolIndex0_y': [45],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [7],
            'T0_toolIndex0_displayTime': [0.2],
            'T0_toolIndex0_y': [40],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [15],
            'T0_toolIndex0_displayTime': [0.9],
            'T0_toolIndex0_y': [50],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [12],
            'T0_toolIndex0_displayTime': [0.8],
            'T0_toolIndex0_y': [65],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [10],
            'T0_toolIndex0_displayTime': [0.9],
            'T0_toolIndex0_y': [50],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [45],
            'T0_toolIndex0_displayTime': [0.4],
            'T0_toolIndex0_y': [25],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [40],
            'T0_toolIndex0_displayTime': [0.6],
            'T0_toolIndex0_y': [30],
        },
    }, {
        'frame0': {
            'T0_toolIndex0_x': [50],
            'T0_toolIndex0_displayTime': [0.5],
            'T0_toolIndex0_y': [20],
        },
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9
    ]
}

processed_data = {
    "frame0": {
        "T0_toolIndex0": [
            (2000, 50, 0.0),
            (15, 45, 0.1),
            (7, 40, 0.2),
            (15, 50, 0.9),
            (12, 65, 0.8),
            (10, 50, 0.9),
            (45, 25, 0.4),
            (40, 30, 0.6),
            (50, 20, 0.5),
        ]
    }
}

reduced_data_hdbscan = {
    "frame0": {
        "T0_toolIndex0_points_x": [2000.0, 15.0, 7.0, 15.0, 12.0, 10.0, 45.0, 40.0, 50.0],
        "T0_toolIndex0_points_y": [50.0, 45.0, 40.0, 50.0, 65.0, 50.0, 25.0, 30.0, 20.0],
        "T0_toolIndex0_points_displayTime": [0.0, 0.1, 0.2, 0.9, 0.8, 0.9, 0.4, 0.6, 0.5],
        "T0_toolIndex0_cluster_labels": [-1, 1, 1, 2, 2, 2, 0, 0, 0],
        "T0_toolIndex0_cluster_probabilities": [0.0, 1.0, 1.0, 1.0, 0.18389844323090718, 1.0, 1.0, 0.9941176470588245, 1.0],
        "T0_toolIndex0_clusters_count": [3, 2, 3],
        "T0_toolIndex0_clusters_x": [45.0, 11.0, 12.333333333333334],
        "T0_toolIndex0_clusters_y": [25.0, 42.5, 55.0],
        "T0_toolIndex0_clusters_displayTime": [0.5, 0.15000000000000002, 0.8666666666666667],
        "T0_toolIndex0_clusters_var_x": [24.97539370078741, 32.0, 10.012699997020526],
        "T0_toolIndex0_clusters_var_y": [24.97539370078741, 12.5, 30.250945982182756],
        "T0_toolIndex0_clusters_var_x_y": [-24.97539370078741, 20.0, -1.0083648660727589],
    },
}

TestShapeReducerTemporalRotateRectangleHdbscan = ReducerTest(
    temporal_point_reducer_hdbscan,
    process_temporal_data,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test temporalPoint reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestTemporalPointReducerHdbscan'
)

reduced_data_dbscan = {
    "frame0": {
        "T0_toolIndex0_points_x": [2000.0, 15.0, 7.0, 15.0, 12.0, 10.0, 45.0, 40.0, 50.0],
        "T0_toolIndex0_points_y": [50.0, 45.0, 40.0, 50.0, 65.0, 50.0, 25.0, 30.0, 20.0],
        "T0_toolIndex0_points_displayTime": [0.0, 0.1, 0.2, 0.9, 0.8, 0.9, 0.4, 0.6, 0.5],
        "T0_toolIndex0_cluster_labels": [-1, 0, 0, 1, -1, 1, 2, 2, 2],
        "T0_toolIndex0_clusters_count": [2, 2, 3],
        "T0_toolIndex0_clusters_x": [11.0, 12.5, 45.0],
        "T0_toolIndex0_clusters_y": [42.5, 50.0, 25.0],
        "T0_toolIndex0_clusters_displayTime": [0.15000000000000002, 0.9, 0.5],
        "T0_toolIndex0_clusters_var_x": [32.0, 12.5, 25.0],
        "T0_toolIndex0_clusters_var_y": [12.5, 0.0, 25.0],
        "T0_toolIndex0_clusters_var_x_y": [20.0, 0.0, -25.0],
    },
}

TestShapeReducerTemporalRotateRectangleDbscan = ReducerTest(
    temporal_point_reducer_dbscan,
    process_temporal_data,
    extracted_data,
    processed_data,
    reduced_data_dbscan,
    'Test temporalPoint reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 200,
        'min_samples': 2,
    },
    test_name='TestTemporalPointReducerDbscan',
)

extracted_data_single_point = classifications = [
    {
        'frame0': {
            'T0_toolIndex0_x': [2000],
            'T0_toolIndex0_displayTime': [0.],
            'T0_toolIndex0_y': [50],
        },
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
    ]
}

processed_data_single_point = {
    "frame0": {
        "T0_toolIndex0": [
            (2000, 50, 0.0)
        ]
    }
}

reduced_data_dbscan_single_point = {
    "frame0": {
        "T0_toolIndex0_points_x": [2000.0],
        "T0_toolIndex0_points_y": [50.0],
        "T0_toolIndex0_points_displayTime": [0.0],
        "T0_toolIndex0_cluster_labels": [0],
        "T0_toolIndex0_clusters_count": [1],
        "T0_toolIndex0_clusters_x": [2000.0],
        "T0_toolIndex0_clusters_y": [50.0],
        "T0_toolIndex0_clusters_displayTime": [0.0],
        "T0_toolIndex0_clusters_var_x": [None],
        "T0_toolIndex0_clusters_var_y": [None],
        "T0_toolIndex0_clusters_var_x_y": [None]
    },
}

TestShapeReducerTemporalRotateRectangleDbscanNoCluster = ReducerTest(
    temporal_point_reducer_dbscan,
    process_temporal_data,
    extracted_data_single_point,
    processed_data_single_point,
    reduced_data_dbscan_single_point,
    'Test temporalPoint reducer with DBSCAN with a single point',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 50,
        'min_samples': 1,
    },
    test_name='TestTemporalPointReducerDbscanSinglePoint',
)
