'''
Polygon As Line Tool for Text Reducer
-------------------------------------
This module provides functions to reduce the polygon-text extractions from
:mod:`panoptes_aggregation.extractors.poly_line_text_extractor`.
'''
from .text_utils import cluster_by_frame
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'eps_slope': {'default': 25.0, 'type': float},
    'eps_line': {'default': 40.0, 'type': float},
    'eps_word': {'default': 40.0, 'type': float},
    'gutter_tol': {'default': 0.0, 'type': float},
    'min_word_count': {'default': 1, 'type': int},
    'dot_freq': {'default': 'word', 'type': str},
    'min_samples': {'default': 1, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}

DEFAULTS_PROCESS = {
    'process_by_line': {'default': False, 'type': bool}
}


def process_data(data_list, process_by_line=False):
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
        with `x`, `y`, `text`, and `slope` keys. `x`, `y`, and `text` are list-of-lists, each inner
        list is from a single annotaiton, `slope` is the list of slopes (in deg) for each of these
        inner lists.
    '''
    data_by_frame = {}
    for data in data_list:
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {})
            data_by_frame[frame].setdefault('x', [])
            data_by_frame[frame].setdefault('y', [])
            data_by_frame[frame].setdefault('text', [])
            data_by_frame[frame].setdefault('slope', [])
            for x, y, t, s in zip(value['points']['x'], value['points']['y'], value['text'], value['slope']):
                if process_by_line:
                    data_by_frame[frame]['x'].append([x[0], x[-1]])
                    data_by_frame[frame]['y'].append([y[0], y[-1]])
                    data_by_frame[frame]['text'].append([' '.join(t)])
                else:
                    data_by_frame[frame]['x'].append(x)
                    data_by_frame[frame]['y'].append(y)
                    data_by_frame[frame]['text'].append(t)
                data_by_frame[frame]['slope'].append(s)
    return data_by_frame


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS, defaults_process=DEFAULTS_PROCESS)
def poly_line_text_reducer(data_by_frame, **kwargs_dbscan):
    '''
    Reduce the polygon-text answers as a list of lines of text.

    Parameters
    ----------
    data_by_frame : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with on key for each `frame` of the subject that have lists as values.
        Each item of the list represents one line transcribed of text and is a dictionary
        with three keys:

        * `clusters_x` : the `x` position of each identified word
        * `clusters_y` : the `y` position of each identified word
        * `clusters_text` : A list of text at each cluster position
        * `gutter_label` : A label indicating what "gutter" cluster the line is from
        * `line_slope`: The slope of the line of text in degrees
        * `slope_label` : A label indicating what slope cluster the line is from
        * `number_views` : The number of users that transcribed the line of text
        * `consensus_score` : The average number of users who's text agreed for the line
            Note, if `consensus_score` is the same a `number_views` every user agreed with each other

        Note: the image coordiate system is left handed with y increasing downward.
    '''
    kwargs_cluster = {}
    kwargs_cluster['eps_slope'] = kwargs_dbscan.pop('eps_slope')
    kwargs_cluster['eps_line'] = kwargs_dbscan.pop('eps_line')
    kwargs_cluster['eps_word'] = kwargs_dbscan.pop('eps_word')
    kwargs_cluster['gutter_tol'] = kwargs_dbscan.pop('gutter_tol')
    kwargs_cluster['dot_freq'] = kwargs_dbscan.pop('dot_freq')
    kwargs_cluster['metric'] = kwargs_dbscan.pop('metric')
    kwargs_cluster['min_word_count'] = kwargs_dbscan.pop('min_word_count')
    return cluster_by_frame(data_by_frame, kwargs_cluster, kwargs_dbscan)
