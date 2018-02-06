'''
Rectangle Reducer
-----------------
This module provides functions to cluster rectangles extracted with
:mod:`panoptes_aggregation.extractors.rectangle_extractor`.
'''
import numpy as np
from sklearn.cluster import DBSCAN
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper

DEFAULTS = {
    'eps': {'default': 5.0, 'type': float},
    'min_samples': {'default': 3, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}


def process_data(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `frame`
    and `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.rectangle_extractor.rectangle_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `frame` dictionary values with keys being
        `tool` with a list of (`x`, `y`, `width`, `height`) tuples as a vlaue
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
                    keys = [
                        '{0}_x'.format(tool),
                        '{0}_y'.format(tool),
                        '{0}_width'.format(tool),
                        '{0}_height'.format(tool)
                    ]
                    if '{0}_tag'.format(tool) in d[frame]:
                        data_by_tool[frame].setdefault('tag', [])
                        data_by_tool[frame]['tag'] += d[frame]['{0}_tag'.format(tool)]
                    if np.all([k in d[frame] for k in keys]):
                        values = list(zip(d[frame][keys[0]], d[frame][keys[1]], d[frame][keys[2]], d[frame][keys[3]]))
                        data_by_tool[frame][tool] += values
    return data_by_tool


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
@subtask_wrapper
def rectangle_reducer(data_by_tool, **kwargs):
    '''Cluster a list of rectangles by tool and frame

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    kwrgs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictinary with the following keys for each frame

        * `tool*_rec_x` : A list of `x` positions for **all** rectangles drawn with `tool*`
        * `tool*_rec_y` : A list of `y` positions for **all** rectangles drawn with `tool*`
        * `tool*_rec_width` : A list of `width` values for **all** rectangles drawn with `tool*`
        * `tool*_rec_height` : A list of `height` values for **all** rectangles drawn with `tool*`
        * `tool*_cluster_labels` : A list of cluster labels for **all** rectangles drawn with `tool*`
        * `tool*_clusters_count` : The number of points in each **cluster** found
        * `tool*_clusters_x` : The `x` position for each **cluster** found
        * `tool*_clusters_y` : The `y` position for each **cluster** found
        * `tool*_clusters_width` : The `widht` value for each **cluster** found
        * `tool*_clusters_height` : The `height` value for each **cluster** found

    '''
    reductions = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        reductions[frame] = OrderedDict()
        if 'tag' in frame_data:
            tags = frame_data.pop('tag')
            reductions[frame]['rec_tags'] = tags
        for tool, loc_list in frame_data.items():
            loc = np.array(loc_list)
            # original data in the order used by clustering code
            reductions[frame]['{0}_rec_x'.format(tool)] = loc[:, 0].tolist()
            reductions[frame]['{0}_rec_y'.format(tool)] = loc[:, 1].tolist()
            reductions[frame]['{0}_rec_width'.format(tool)] = loc[:, 2].tolist()
            reductions[frame]['{0}_rec_height'.format(tool)] = loc[:, 3].tolist()
            reductions[frame]['{0}_cluster_labels'.format(tool)] = [-1] * loc.shape[0]
            if loc.shape[0] >= kwargs['min_samples']:
                db = DBSCAN(**kwargs).fit(loc)
                reductions[frame]['{0}_cluster_labels'.format(tool)] = db.labels_.tolist()
                for k in set(db.labels_):
                    if k > -1:
                        idx = db.labels_ == k
                        reductions[frame].setdefault('{0}_clusters_count'.format(tool), []).append(int(idx.sum()))
                        k_loc = loc[idx].mean(axis=0)
                        reductions[frame].setdefault('{0}_clusters_x'.format(tool), []).append(float(k_loc[0]))
                        reductions[frame].setdefault('{0}_clusters_y'.format(tool), []).append(float(k_loc[1]))
                        reductions[frame].setdefault('{0}_clusters_width'.format(tool), []).append(float(k_loc[2]))
                        reductions[frame].setdefault('{0}_clusters_height'.format(tool), []).append(float(k_loc[3]))
    return reductions
