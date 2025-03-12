import numpy as np
from panoptes_aggregation.reducers.point_reducer_dbscan import process_data_by_frame, point_reducer_dbscan
from .base_test_class import ReducerTestPoints

c0_cov = np.array([[3, 0.5], [0.5, 4]]).tolist()
c1_cov = np.array([[7, -0.5], [-0.5, 5]]).tolist()
c0_loc = np.array([12, 15]).tolist()
c1_loc = np.array([20, 25]).tolist()
c0_count = 15
c1_count = 8
np.random.seed(5000)
xy = np.vstack([
    np.random.multivariate_normal(c0_loc, c0_cov, size=c0_count),
    np.random.multivariate_normal(c1_loc, c1_cov, size=c1_count)
])
# Reformat to list
xy = xy.T.tolist()
extracted_data = [
    {
        'frame0': {
            'tool1_x': list(xy[0][:12]),
            'tool1_y': list(xy[1][:12]),
            'tool2_x': [3, None, None],
            'tool2_y': [4, None, None]
        }
    },
    {
        'frame0': {
            'tool1_x': list(xy[0][12:]),
            'tool1_y': list(xy[1][12:]),
        }
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
        2
    ]
}

processed_data = {
    'frame0': {
        'tool1': [tuple((xy[0][i], xy[1][i])) for i in range(len(xy[0]))],
        'tool2': [(3, 4), (None, None), (None, None)]
    }
}
reduced_data = {
    'frame0': {
        'tool1_points_x': list(xy[0]),
        'tool1_points_y': list(xy[1]),
        'tool1_cluster_labels': [0] * c0_count + [1] * c1_count,
        'tool1_clusters_count': [c0_count, c1_count],
        'tool1_clusters_x': [c0_loc[0], c1_loc[0]],
        'tool1_clusters_y': [c0_loc[1], c1_loc[1]],
        'tool1_clusters_var_x': [c0_cov[0][0], c1_cov[0][0]],
        'tool1_clusters_var_y': [c0_cov[1][1], c1_cov[1][1]],
        'tool1_clusters_var_x_y': [c0_cov[0][1], c1_cov[0][1]],
        'tool2_points_x': [3],
        'tool2_points_y': [4],
        'tool2_cluster_labels': [-1]
    }
}

TestPointsCluster = ReducerTestPoints(
    point_reducer_dbscan,
    process_data_by_frame,
    extracted_data,
    processed_data,
    reduced_data,
    'Test point reducer DBSCAN',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 3
    },
    atol=2,
    test_name='TestPointsCluster'
)

extracted_data_one_point = [
    {
        'frame0': {
            'tool1_x': [0],
            'tool1_y': [0]
        }
    }
]
kwargs_extra_data_one_point = {
    'user_id': [
        1
    ]
}
processed_data_one_point = {
    'frame0': {
        'tool1': [(0, 0)]
    }
}
reduced_data_one_point = {
    'frame0': {
        'tool1_points_x': [0],
        'tool1_points_y': [0],
        'tool1_cluster_labels': [0],
        'tool1_clusters_count': [1],
        'tool1_clusters_x': [0],
        'tool1_clusters_y': [0],
        'tool1_clusters_var_x': [None],
        'tool1_clusters_var_y': [None],
        'tool1_clusters_var_x_y': [None]
    }
}

TestOnePointCluster = ReducerTestPoints(
    point_reducer_dbscan,
    process_data_by_frame,
    extracted_data_one_point,
    processed_data_one_point,
    reduced_data_one_point,
    'Test point reducer DBSCAN with one data point',
    network_kwargs=kwargs_extra_data_one_point,
    kwargs={
        'eps': 5,
        'min_samples': 1
    },
    atol=2,
    test_name='TestOnePointCluster'
)
