'''
Point Reducer DBSCAN
--------------------
This module provides functions to cluster points extracted with
:mod:`panoptes_aggregation.extractors.point_extractor`.
'''
import numpy as np
from sklearn.cluster import DBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper
from .point_process_data import process_data_by_frame


DEFAULTS = {
    'eps': {'default': 5.0, 'type': float},
    'min_samples': {'default': 3, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}


@reducer_wrapper(process_data=process_data_by_frame, defaults_data=DEFAULTS, user_id=True)
@subtask_wrapper
def point_reducer_dbscan(data_by_tool, **kwargs):
    '''Cluster a list of points by tool using DBSCAN

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with one key per subject `frame`.  Each frame has the following keys

        * `tool*_points_x` : A list of `x` positions for **all** points drawn with `tool*`
        * `tool*_points_y` : A list of `y` positions for **all** points drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** points drawn with `tool*`
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_x` : The `x` position for each **cluster** found
        * `tool*_clusters_y` : The `y` position for each **cluster** found
        * `tool*_clusters_var_x` : The `x` variance of points in each **cluster** found
        * `tool*_clusters_var_y` : The `y` variance of points in each **cluster** found
        * `tool*_clusters_var_x_y` : The `x-y` covariance of points in each **cluster** found

    '''
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, loc_list in frame_data.items():
            # clean `None` values for the list
            loc_list_clean = [xy for xy in loc_list if None not in xy]
            loc = np.array(loc_list_clean)
            # original data points in order used by cluster code
            clusters[frame]['{0}_points_x'.format(tool)] = loc[:, 0].tolist()
            clusters[frame]['{0}_points_y'.format(tool)] = loc[:, 1].tolist()
            # default each point in no cluster
            clusters[frame]['{0}_cluster_labels'.format(tool)] = [-1] * loc.shape[0]
            if loc.shape[0] >= kwargs['min_samples']:
                db = DBSCAN(**kwargs).fit(loc)
                # what cluster each point belongs to
                clusters[frame]['{0}_cluster_labels'.format(tool)] = db.labels_.tolist()
                for k in set(db.labels_):
                    if k > -1:
                        idx = db.labels_ == k
                        # number of points in the cluster
                        clusters[frame].setdefault('{0}_clusters_count'.format(tool), []).append(int(idx.sum()))
                        # mean of the cluster
                        k_loc = loc[idx].mean(axis=0)
                        clusters[frame].setdefault('{0}_clusters_x'.format(tool), []).append(float(k_loc[0]))
                        clusters[frame].setdefault('{0}_clusters_y'.format(tool), []).append(float(k_loc[1]))
                        # cov matrix of the cluster
                        if idx.sum() > 1:
                            k_cov = np.cov(loc[idx].T)
                            clusters[frame].setdefault('{0}_clusters_var_x'.format(tool), []).append(float(k_cov[0, 0]))
                            clusters[frame].setdefault('{0}_clusters_var_y'.format(tool), []).append(float(k_cov[1, 1]))
                            clusters[frame].setdefault('{0}_clusters_var_x_y'.format(tool), []).append(float(k_cov[0, 1]))
                        else:
                            clusters[frame].setdefault('{0}_clusters_var_x'.format(tool), []).append(None)
                            clusters[frame].setdefault('{0}_clusters_var_y'.format(tool), []).append(None)
                            clusters[frame].setdefault('{0}_clusters_var_x_y'.format(tool), []).append(None)
    return clusters
