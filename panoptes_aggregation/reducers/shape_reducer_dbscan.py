'''
Shape Reducer DBSCAN
--------------------
This module provides functions to cluster shapes extracted with
:mod:`panoptes_aggregation.extractors.shape_extractor`.
'''
import numpy as np
from sklearn.cluster import DBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper
from ..shape_tools import SHAPE_LUT
from .shape_process_data import process_data, DEFAULTS_PROCESS
from .shape_metric import get_shape_metric_and_avg
from .shape_metric_IoU import IoU_metric, average_shape_IoU

DEFAULTS = {
    'eps': {'default': 5.0, 'type': float},
    'eps_t': {'default': 0.5, 'type': float},
    'min_samples': {'default': 3, 'type': int},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float},
    'metric_type': {'default': 'euclidean', 'type': str},
    'estimate_average': {'default': False, 'type': bool}
}


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    defaults_process=DEFAULTS_PROCESS,
    user_id=True
)
@subtask_wrapper
def shape_reducer_dbscan(data_by_tool, **kwargs):
    '''Cluster a shape by tool using DBSCAN

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

    estimate_average : bool
        For the IoU metric estimate the average by the most representative shape from the cluster,
        this is significantly faster to compute than the true average, True by default.

    kwargs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with the following keys for each frame

        * `tool*_<shape>_<param>` : A list of **all** `param` for the `shape` drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** shapes drawn with `tool*`
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_<param>` : The `param` value for each **cluster** found

        If the "IoU" metric type is used there is also

        * `tool*_clusters_sigma` : The standard deviation of the average shape under the IoU metric
    '''
    shape = data_by_tool.pop('shape')
    eps_t = kwargs.pop('eps_t', None)
    estimate_average = kwargs.pop('estimate_average', DEFAULTS['estimate_average']['default'])
    shape_params = SHAPE_LUT[shape]
    metric_type = kwargs.pop('metric_type', 'euclidean').lower()
    symmetric = data_by_tool.pop('symmetric')
    if metric_type == 'euclidean':
        metric, avg = get_shape_metric_and_avg(shape, symmetric=symmetric)
        kwargs['metric'] = metric
    elif metric_type == 'iou':
        kwargs['metric'] = IoU_metric
        kwargs['metric_params'] = {'shape': shape, 'eps_t': eps_t}
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
                        if metric_type == 'euclidean':
                            k_loc = avg(loc[idx])
                        elif metric_type == 'iou':
                            k_loc, sigma = avg(loc[idx], shape, eps_t, estimate=estimate_average)
                            clusters[frame].setdefault('{0}_clusters_sigma'.format(tool), []).append(float(sigma))
                        for pdx, param in enumerate(shape_params):
                            clusters[frame].setdefault('{0}_clusters_{1}'.format(tool, param), []).append(float(k_loc[pdx]))
    return clusters
