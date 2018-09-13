'''
Point Reducer HDBSCAN
---------------------
This module provides functions to cluster points extracted with
:mod:`panoptes_aggregation.extractors.point_extractor`.
'''
import numpy as np
from hdbscan import HDBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper


DEFAULTS = {
    'min_cluster_size': {'default': 5, 'type': int},
    'min_samples': {'default': 3, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'best', 'type': str},
    'leaf_size': {'default': 40, 'type': int},
    'p': {'default': None, 'type': float},
    'cluster_selection_method': {'default': 'eom', 'type': str},
    'allow_single_cluster': {'default': False, 'type': bool}
}


def process_data(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

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
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {}
    for frame in unique_frames:
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for d in data:
                if frame in d:
                    data_by_tool[frame].setdefault(tool, [])
                    if ('{0}_x'.format(tool) in d[frame]) and ('{0}_y'.format(tool) in d[frame]):
                        data_by_tool[frame][tool] += list(zip(d[frame]['{0}_x'.format(tool)], d[frame]['{0}_y'.format(tool)]))
    return data_by_tool


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
@subtask_wrapper
def point_reducer_hdbscan(data_by_tool, **kwargs):
    '''Cluster a list of points by tool using HDBSCAN

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    kwrgs :
        `See HDBSCAN <http://hdbscan.readthedocs.io/en/latest/api.html#hdbscan>`_

    Returns
    -------
    reduction : dict
        A dictinary with one key per subject `frame`.  Each frame has the following keys

        * `tool*_points_x` : A list of `x` positions for **all** points drawn with `tool*`
        * `tool*_points_y` : A list of `y` positions for **all** points drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** points drawn with `tool*`
        * `tool*_cluster_probabilities`: A list of cluster probabilities for **all** points drawn with `tool*`
        * `tool*_clusters_persistance`: A mesure for how persistent each **cluster** is (1.0 = stable, 0.0 = unstable)
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_x` : The weighted `x` position for each **cluster** found
        * `tool*_clusters_y` : The weighted `y` position for each **cluster** found
        * `tool*_clusters_var_x` : The weighted `x` varaince of points in each **cluster** found
        * `tool*_clusters_var_y` : The weighted `y` varaince of points in each **cluster** found
        * `tool*_clusters_var_x_y` : The weighted `x-y` covaraince of points in each **cluster** found

    '''
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, loc_list in frame_data.items():
            # clean `None` values for the list
            loc_list_clean = [xy for xy in loc_list if None not in xy]
            loc = np.array(loc_list_clean)
            # orignal data points in order used by cluster code
            clusters[frame]['{0}_points_x'.format(tool)] = list(loc[:, 0])
            clusters[frame]['{0}_points_y'.format(tool)] = list(loc[:, 1])
            # default each point in no cluster
            clusters[frame]['{0}_cluster_labels'.format(tool)] = [-1] * loc.shape[0]
            clusters[frame]['{0}_cluster_probabilities'.format(tool)] = [0] * loc.shape[0]
            if loc.shape[0] >= kwargs['min_cluster_size']:
                db = HDBSCAN(**kwargs).fit(loc)
                # what cluster each point belongs to
                clusters[frame]['{0}_cluster_labels'.format(tool)] = list(db.labels_)
                clusters[frame]['{0}_cluster_probabilities'.format(tool)] = list(db.probabilities_)
                clusters[frame]['{0}_clusters_persistance'.format(tool)] = list(db.cluster_persistence_)
                for k in set(db.labels_):
                    if k > -1:
                        idx = db.labels_ == k
                        # number of points in the cluster
                        clusters[frame].setdefault('{0}_clusters_count'.format(tool), []).append(int(idx.sum()))
                        # mean of the cluster
                        weights = db.probabilities_[idx]
                        k_loc = np.average(loc[idx], axis=0, weights=weights)
                        k_loc = loc[idx].mean(axis=0)
                        clusters[frame].setdefault('{0}_clusters_x'.format(tool), []).append(float(k_loc[0]))
                        clusters[frame].setdefault('{0}_clusters_y'.format(tool), []).append(float(k_loc[1]))
                        # cov matrix of the cluster
                        k_cov = np.cov(loc[idx].T, aweights=weights)
                        clusters[frame].setdefault('{0}_clusters_var_x'.format(tool), []).append(float(k_cov[0, 0]))
                        clusters[frame].setdefault('{0}_clusters_var_y'.format(tool), []).append(float(k_cov[1, 1]))
                        clusters[frame].setdefault('{0}_clusters_var_x_y'.format(tool), []).append(float(k_cov[0, 1]))
    return clusters
