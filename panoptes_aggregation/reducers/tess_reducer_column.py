'''
TESS Column Reducer
-------------------
This module porvides functions to reduce the column task extracts for the TESS project.
Extracts are from :mod:`panoptes_aggregation.extractors.shape_extractor`.
'''
from .reducer_wrapper import reducer_wrapper
from ..shape_tools import SHAPE_LUT
from collections import OrderedDict
from sklearn.cluster import DBSCAN
import numpy as np

DEFAULTS = {
    'x': {'default': 'center', 'type': str},
    'eps': {'default': 5.0, 'type': float},
    'min_samples': {'default': 3, 'type': int},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}


def process_data(data, **kwargs_extra_data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.shape_extractor.shape_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with two keys

        * `data`: An Nx2 numpy array containing the *center* and width of each column drawn
        * `index`: A list of lenght N indicating the extract index for each drawn column
    '''
    shape_params = SHAPE_LUT['column']
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = []
    index_by_tool = []
    for frame in unique_frames:
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for ddx, d in enumerate(data):
                if frame in d:
                    keys = ['{0}_{1}'.format(tool, param) for param in shape_params]
                    if np.all([k in d[frame] for k in keys]):
                        params_list = list(zip(*(d[frame][k] for k in keys)))
                        index_by_tool += [ddx] * len(params_list)
                        data_by_tool += params_list
    return {'data': data_by_tool, 'index': index_by_tool}


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS, user_id=True, relevant_reduction=True)
def tess_reducer_column(data_by_tool, **kwargs):
    '''Cluster TESS columns using DBSCAN

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    user_id : keyword, list
        A list containing the user IDs for each extract
    relevant_reduction : keyword, list
        A list containing the TESS user reduction for each extract
        :meth:`panoptes_aggregation.running_reducers.tess_user_reducer.tess_user_reducer`
    x : keyword, str
        Either `"center"` or `"left"` and indicates if the `x` value of the classification
        is the center or left side of the column
    kwrgs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictinary with the following keys

        * `centers` : A list with the center `x` position for all identified columns
        * `widths` : A list with the full width of all identified columns
        * `counts` : A list with the number of volunteers who identified each column
        * `weighted_counts` : A list with the weighted number of volunteers who identified each column
        * `user_ids`: A list of lists with the `user_id` for each volunteer who marked each column
    '''
    user_id = np.array(kwargs.pop('user_id'))
    relevant_reduction = kwargs.pop('relevant_reduction')
    skill = np.array([rr['data']['skill'] for rr in relevant_reduction])
    clusters = OrderedDict()
    loc = np.array(data_by_tool['data'])
    index = np.array(data_by_tool['index'])
    x = kwargs.pop('x')
    if x == 'left':
        loc[:, 0] += 0.5 * loc[:, 1]
    if loc.shape[0] >= kwargs['min_samples']:
        db = DBSCAN(**kwargs).fit(loc)
        for k in set(db.labels_):
            if k > -1:
                idx = db.labels_ == k
                # center and width of the cluster
                k_loc = loc[idx].mean(axis=0)
                clusters.setdefault('centers', []).append(float(k_loc[0]))
                clusters.setdefault('widths', []).append(float(k_loc[1]))
                # number of points in the cluster
                clusters.setdefault('counts', []).append(int(idx.sum()))
                # weighted number of points in the cluster
                k_skill = [skill[j] for j in index[idx]]
                clusters.setdefault('weighted_counts', []).append(float(sum(k_skill)))
                # user_ids in the cluster
                k_users = [user_id[j] for j in index[idx]]
                clusters.setdefault('user_ids', []).append(k_users)
    return clusters
