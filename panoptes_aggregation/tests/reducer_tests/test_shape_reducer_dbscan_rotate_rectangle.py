from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data, shape_reducer_dbscan
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [60.0, 20.0],
            'T0_tool0_angle': [179.0, -179.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [60.0, 20.0],
            'T0_tool0_angle': [-179.0, 179.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [50.0, 10.0],
            'T0_tool1_angle': [179.0, -179.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0],
            'T0_tool1_angle': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [50.0, 10.0],
            'T0_tool1_angle': [-179.0, 179.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_width': [20.0],
            'T0_tool0_height': [20.0],
            'T0_tool0_angle': [20.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'rotateRectangle',
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0, 179.0),
            (100.0, 100.0, 10.0, 20.0, -179.0),
            (0.0, 0.0, 50.0, 60.0, -179.0),
            (100.0, 100.0, 10.0, 20.0, 179.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0, 179.0),
            (100.0, 0.0, 50.0, 10.0, -179.0),
            (0.0, 100.0, 10.0, 50.0, -179.0),
            (100.0, 0.0, 50.0, 10.0, 179.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_rotateRectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rotateRectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rotateRectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rotateRectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_rotateRectangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [60.0, 20.0],
        'T0_tool0_clusters_angle': [180.0, 180.0],
        'T0_tool1_rotateRectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rotateRectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rotateRectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rotateRectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_rotateRectangle_angle': [179.0, -179.0, -179.0, 179.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [50.0, 10.0],
        'T0_tool1_clusters_angle': [180.0, 180.0]
    },
    'frame1': {
        'T0_tool0_rotateRectangle_x': [20.0],
        'T0_tool0_rotateRectangle_y': [20.0],
        'T0_tool0_rotateRectangle_width': [20.0],
        'T0_tool0_rotateRectangle_height': [20.0],
        'T0_tool0_rotateRectangle_angle': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rotateRectangle_x': [50.0, 50.0],
        'T0_tool1_rotateRectangle_y': [50.0, 50.0],
        'T0_tool1_rotateRectangle_width': [50.0, 50.0],
        'T0_tool1_rotateRectangle_height': [50.0, 50.0],
        'T0_tool1_rotateRectangle_angle': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
        'T0_tool1_clusters_angle': [50.0]
    }
}

TestShapeReducerRotateRectangle = ReducerTest(
    shape_reducer_dbscan,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rotateRectangle reducer',
    pkwargs={'shape': 'rotateRectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)
