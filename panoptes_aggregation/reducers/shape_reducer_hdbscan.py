'''
Shape Reducer HDBSCAN
---------------------
This module provides functions to cluster shapes extracted with
:mod:`panoptes_aggregation.extractors.shape_extractor`.
'''
import numpy as np
from hdbscan import HDBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper
from ..shape_tools import SHAPE_LUT
from .angle_utils import angle_euclidean_metric, angle_mean


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

DEFAULTS_PROCESS = {
    'shape': {'default': None, 'type': str}
}


def process_data(data, shape=None):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.shape_extractor.shape_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`, ...)
        tuples as a vlaue. Each shape parameter shows up in this list.
    '''
    if shape is None:
        raise KeyError('`shape` must be provided as a keyword')
    if shape not in SHAPE_LUT:
        raise KeyError('`shape` must be one of {0}'.format(list(SHAPE_LUT.keys())))
    shape_params = SHAPE_LUT[shape]
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {'shape': shape}
    for frame in unique_frames:
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for d in data:
                if frame in d:
                    data_by_tool[frame].setdefault(tool, [])
                    keys = ['{0}_{1}'.format(tool, param) for param in shape_params]
                    if np.all([k in d[frame] for k in keys]):
                        data_by_tool[frame][tool] += list(zip(*(d[frame][k] for k in keys)))
    return data_by_tool


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS, defaults_process=DEFAULTS_PROCESS)
@subtask_wrapper
def shape_reducer_hdbscan(data_by_tool, **kwargs):
    '''Cluster a shape by tool using HDBSCAN

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    kwrgs :
        `See HDBSCAN <http://hdbscan.readthedocs.io/en/latest/api.html#hdbscan>`_

    Returns
    -------
    reduction : dict
        A dictinary with the following keys for each frame

        * `tool*_<shape>_<param>` : A list of **all** `param` for the `sahpe` drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** shapes drawn with `tool*`
        * `tool*_cluster_probabilities`: A list of cluster probabilities for **all** points drawn with `tool*`
        * `tool*_clusters_persistance`: A mesure for how persistent each **cluster** is (1.0 = stable, 0.0 = unstable)
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_<param>` : The `param` value for each **cluster** found
    '''
    shape = data_by_tool.pop('shape')
    shape_params = SHAPE_LUT[shape]
    angle = False
    if shape_params[-1] in ['angle', 'rotation']:
        kwargs['metric'] = angle_euclidean_metric
        angle = True
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, loc_list in frame_data.items():
            loc = np.array(loc_list)
            if len(shape_params) == 1:
                loc = loc.reshape(-1, 1)
            # orignal data points in order used by cluster code
            for pdx, param in enumerate(shape_params):
                clusters[frame]['{0}_{1}_{2}'.format(tool, shape, param)] = loc[:, pdx].tolist()
            # default each point in no cluster
            clusters[frame]['{0}_cluster_labels'.format(tool)] = [-1] * loc.shape[0]
            clusters[frame]['{0}_cluster_probabilities'.format(tool)] = [0] * loc.shape[0]
            if loc.shape[0] >= kwargs['min_cluster_size']:
                db = HDBSCAN(**kwargs).fit(loc)
                # what cluster each point belongs to
                clusters[frame]['{0}_cluster_labels'.format(tool)] = db.labels_.tolist()
                clusters[frame]['{0}_cluster_probabilities'.format(tool)] = list(db.probabilities_)
                clusters[frame]['{0}_clusters_persistance'.format(tool)] = list(db.cluster_persistence_)
                for k in set(db.labels_):
                    if k > -1:
                        idx = db.labels_ == k
                        # number of points in the cluster
                        clusters[frame].setdefault('{0}_clusters_count'.format(tool), []).append(int(idx.sum()))
                        # mean of the cluster
                        k_loc = angle_mean(loc[idx], angle=angle, kind=shape_params[-1])
                        for pdx, param in enumerate(shape_params):
                            clusters[frame].setdefault('{0}_clusters_{1}'.format(tool, param), []).append(float(k_loc[pdx]))
    return clusters
