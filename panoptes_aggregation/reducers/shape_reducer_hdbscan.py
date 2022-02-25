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
from .shape_process_data import process_data, DEFAULTS_PROCESS
from .shape_metric import get_shape_metric_and_avg
from .shape_metric_IoU import IoU_metric, average_shape_IoU


DEFAULTS = {
    'min_cluster_size': {'default': 5, 'type': int},
    'min_samples': {'default': 3, 'type': int},
    'algorithm': {'default': 'best', 'type': str},
    'leaf_size': {'default': 40, 'type': int},
    'p': {'default': None, 'type': float},
    'cluster_selection_method': {'default': 'eom', 'type': str},
    'allow_single_cluster': {'default': False, 'type': bool},
    'metric_type': {'default': 'euclidean', 'type': str}
}


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    defaults_process=DEFAULTS_PROCESS,
    user_id=True
)
@subtask_wrapper
def shape_reducer_hdbscan(data_by_tool, **kwargs):
    '''Cluster a shape by tool using HDBSCAN

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    metric_type : str
        Either "euclidean" to use a euclidean metric in the N-dimension shape parameter space
        or "IoU" for the intersection of union metric based on shape overlap.  The IoU metric
        can only be used with the following shape:

        * rectangle
        * rotateRectangle
        * circle
        * ellipse

    kwargs :
        `See HDBSCAN <http://hdbscan.readthedocs.io/en/latest/api.html#hdbscan>`_

    Returns
    -------
    reduction : dict
        A dictionary with the following keys for each frame

        * `tool*_<shape>_<param>` : A list of **all** `param` for the `shape` drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** shapes drawn with `tool*`
        * `tool*_cluster_probabilities`: A list of cluster probabilities for **all** points drawn with `tool*`
        * `tool*_clusters_persistance`: A measure for how persistent each **cluster** is (1.0 = stable, 0.0 = unstable)
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_<param>` : The `param` value for each **cluster** found

        If the "IoU" metric type is used there is also

        * `tool*_clusters_sigma` : The standard deviation of the average shape under the IoU metric
    '''
    shape = data_by_tool.pop('shape')
    shape_params = SHAPE_LUT[shape]
    metric_type = kwargs.pop('metric_type', 'euclidean').lower()
    symmetric = data_by_tool.pop('symmetric')
    if metric_type == 'euclidean':
        metric, avg = get_shape_metric_and_avg(shape, symmetric=symmetric)
        kwargs['metric'] = metric
    elif metric_type == 'iou':
        kwargs['metric'] = IoU_metric
        kwargs['shape'] = shape
        avg = average_shape_IoU
    else:
        raise ValueError('metric_type must be either "euclidean" or "IoU".')
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, loc_list in frame_data.items():
            loc = np.array(loc_list)
            if len(shape_params) == 1:
                loc = loc.reshape(-1, 1)
            # original data points in order used by cluster code
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
                        if metric_type == 'euclidean':
                            k_loc = avg(loc[idx])
                        elif metric_type == 'iou':
                            k_loc, sigma = avg(loc[idx], shape)
                            clusters[frame].setdefault('{0}_clusters_sigma'.format(tool), []).append(float(sigma))
                        for pdx, param in enumerate(shape_params):
                            clusters[frame].setdefault('{0}_clusters_{1}'.format(tool, param), []).append(float(k_loc[pdx]))
    return clusters
