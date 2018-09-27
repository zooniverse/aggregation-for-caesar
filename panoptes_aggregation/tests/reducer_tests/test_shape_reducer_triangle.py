from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_r': [50.0, 10.0],
            'T0_tool0_angle': [179.0, -179.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_r': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_r': [50.0, 10.0],
            'T0_tool0_angle': [-179.0, 179.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_r': [10.0, 50.0],
            'T0_tool1_angle': [179.0, -179.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_r': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_r': [10.0, 50.0],
            'T0_tool1_angle': [-179.0, 179.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_r': [20.0],
            'T0_tool0_angle': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'triangle',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 179.0),
            (100.0, 100.0, 10.0, -179.0),
            (0.0, 0.0, 50.0, -179.0),
            (100.0, 100.0, 10.00, 179.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 179.0),
            (100.0, 0.0, 50.0, -179.0),
            (0.0, 100.0, 10.0, -179.0),
            (100.0, 0.0, 50.0, 179.0)
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
        'T0_tool0_triangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_triangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_triangle_r': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_triangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_r': [50.0, 10.0],
        'T0_tool0_clusters_angle': [180.0, 180.0],
        'T0_tool1_triangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_triangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_triangle_r': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_triangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_r': [10.0, 50.0],
        'T0_tool1_clusters_angle': [180.0, 180.0]
    },
    'frame1': {
        'T0_tool0_triangle_x': [20.0],
        'T0_tool0_triangle_y': [20.0],
        'T0_tool0_triangle_r': [20.0],
        'T0_tool0_triangle_angle': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_triangle_x': [50.0, 50.0],
        'T0_tool1_triangle_y': [50.0, 50.0],
        'T0_tool1_triangle_r': [50.0, 50.0],
        'T0_tool1_triangle_angle': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_r': [50.0],
        'T0_tool1_clusters_angle': [50.0]
    }
}

TestShapeReducerRotateRectangle = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape triangle reducer with DBSCAN',
    pkwargs={'shape': 'triangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)

reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool0_clusters_persistance'] = [0.9863917236512045, 0.9863917236512045]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_clusters_persistance'] = [0.9863917236512045, 0.9863917236512045]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool1_clusters_persistance'] = [1.0]

TestShapeReducerTriangleHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape triangle reducer with HDBSCAN',
    pkwargs={'shape': 'triangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    }
)
