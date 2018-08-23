'''
Point Reducer
-------------
This module provides functions to cluster points extracted with
:mod:`panoptes_aggregation.extractors.point_extractor`.
'''
import numpy as np
from sklearn.cluster import DBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper


DEFAULTS = {
    'eps': {'default': 5.0, 'type': float},
    'min_samples': {'default': 3, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}


def process_data(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`.

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.point_extractor.point_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`)
        tuples as a vlaue
    '''
    unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.keys()] for d in data], []))
    data_by_tool = {}
    for tool in unique_tools:
        for d in data:
            data_by_tool.setdefault(tool, [])
            if ('{0}_x'.format(tool) in d) and ('{0}_y'.format(tool) in d):
                data_by_tool[tool] += list(zip(d['{0}_x'.format(tool)], d['{0}_y'.format(tool)]))
    return data_by_tool


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
def point_reducer(data_by_tool, **kwargs):
    '''Cluster a list of points by tool using DBSCAN

    This reducer is for use with :mod:`panoptes_aggregation.extractors.point_extractor`
    that does *not* seperate points by `frame` and does not support subtask reduction.  Use
    :mod:`panoptes_aggregation.extractors.point_extractor_by_frame`  and
    :mod:`panoptes_aggregation.reducers.point_reducer_dbscan` if there
    are multiple frames *or* subtasks.

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    kwrgs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictinary with the following keys

        * `tool*_points_x` : A list of `x` positions for **all** points drawn with `tool*`
        * `tool*_points_y` : A list of `y` positions for **all** points drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** points drawn with `tool*`
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_x` : The `x` position for each **cluster** found
        * `tool*_clusters_y` : The `y` position for each **cluster** found
        * `tool*_clusters_var_x` : The `x` varaince of points in each **cluster** found
        * `tool*_clusters_var_y` : The `y` varaince of points in each **cluster** found
        * `tool*_clusters_var_x_y` : The `x-y` covaraince of points in each **cluster** found

    '''
    clusters = OrderedDict()
    for tool, loc_list in data_by_tool.items():
        # clean `None` values for the list
        loc_list_clean = [xy for xy in loc_list if None not in xy]
        loc = np.array(loc_list_clean)
        # orignal data points in order used by cluster code
        clusters['{0}_points_x'.format(tool)] = list(loc[:, 0])
        clusters['{0}_points_y'.format(tool)] = list(loc[:, 1])
        # default each point in no cluster
        clusters['{0}_cluster_labels'.format(tool)] = [-1] * loc.shape[0]
        if loc.shape[0] >= kwargs['min_samples']:
            db = DBSCAN(**kwargs).fit(loc)
            # what cluster each point belongs to
            clusters['{0}_cluster_labels'.format(tool)] = list(db.labels_)
            for k in set(db.labels_):
                if k > -1:
                    idx = db.labels_ == k
                    # number of points in the cluster
                    clusters.setdefault('{0}_clusters_count'.format(tool), []).append(int(idx.sum()))
                    # mean of the cluster
                    k_loc = loc[idx].mean(axis=0)
                    clusters.setdefault('{0}_clusters_x'.format(tool), []).append(float(k_loc[0]))
                    clusters.setdefault('{0}_clusters_y'.format(tool), []).append(float(k_loc[1]))
                    # cov matrix of the cluster
                    if idx.sum() > 1:
                        k_cov = np.cov(loc[idx].T)
                        clusters.setdefault('{0}_clusters_var_x'.format(tool), []).append(float(k_cov[0, 0]))
                        clusters.setdefault('{0}_clusters_var_y'.format(tool), []).append(float(k_cov[1, 1]))
                        clusters.setdefault('{0}_clusters_var_x_y'.format(tool), []).append(float(k_cov[0, 1]))
                    else:
                        clusters.setdefault('{0}_clusters_var_x'.format(tool), []).append(None)
                        clusters.setdefault('{0}_clusters_var_y'.format(tool), []).append(None)
                        clusters.setdefault('{0}_clusters_var_x_y'.format(tool), []).append(None)
    return clusters
