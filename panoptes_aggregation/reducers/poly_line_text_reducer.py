'''
Polygon As Line Tool for Text Reducer
-------------------------------------
This module provides functions to reduce the polygon-text extractions from
:mod:`panoptes_aggregation.extractors.poly_line_text_extractor`.
'''
import numpy as np
from .point_reducer import point_reducer, DEFAULTS
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper


def process_data(data_list):
    '''Process a list of extractions into a dictionary of `loc` and `text`
    organized by `frame`

    Parameters
    ----------
    data_list : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.poly_line_text_extractor.poly_line_text_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with keys for each `frame` of the subject and values being dictionaries
        with `loc` (a list of (`x`, `y`) tuples) and `text` (a list of strings) keys.
    '''
    data_by_frame = {}
    for data in data_list:
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {})
            data_by_frame[frame].setdefault('loc', [])
            data_by_frame[frame].setdefault('text', [])
            for x, y, t in zip(value['points']['x'], value['points']['y'], value['text']):
                data_by_frame[frame]['loc'].append((x, y))
                data_by_frame[frame]['text'].append(t)
    return data_by_frame


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
def poly_line_text_reducer(data_by_frame, **kwargs):
    '''
    Parameters
    ----------
    data_by_frame : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with on key for each `frame` of the subject that have dictionaries as values.
        Those dictionaries have three keys:

        * `clusters_x` : the `x` position of each identified cluster
        * `clusters_y` : the `y` position of each identified cluster
        * `clusters_text` : A list of text as ecah clster position
    '''
    reduced_data = OrderedDict()
    data_by_frame_locs = {}
    for frame, value in data_by_frame.items():
        data_by_frame_locs[frame] = value['loc']
    full_cluster_data = point_reducer._original(data_by_frame_locs, **kwargs)
    for frame in sorted(data_by_frame.keys()):
        reduced_data[frame] = OrderedDict()
        reduced_data[frame]['clusters_x'] = full_cluster_data['{0}_clusters_x'.format(frame)]
        reduced_data[frame]['clusters_y'] = full_cluster_data['{0}_clusters_y'.format(frame)]
        reduced_data[frame]['clusters_text'] = []
        labels = np.array(full_cluster_data['{0}_cluster_labels'.format(frame)])
        for k in set(labels):
            kdx = labels == k
            text_list = list(np.array(data_by_frame[frame]['text'])[kdx])
            reduced_data[frame]['clusters_text'].append(text_list)
    return reduced_data
