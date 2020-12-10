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
    'dot_freq': {'default': 'line', 'type': str},
    'min_samples': {'default': 1, 'type': int},
    'low_consensus_threshold': {'default': 3, 'type': float},
    'minimum_views': {'default': 5, 'type': int}
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
    for data_index, data in enumerate(data_list):
        for frame, value in data.items():
            gs = value.get('gold_standard', False)
            data_by_frame.setdefault(frame, {})
            data_by_frame[frame].setdefault('x', [])
            data_by_frame[frame].setdefault('y', [])
            data_by_frame[frame].setdefault('text', [])
            data_by_frame[frame].setdefault('slope', [])
            data_by_frame[frame].setdefault('gold_standard', [])
            data_by_frame[frame].setdefault('data_index', [])
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
                data_by_frame[frame]['gold_standard'].append(gs)
                data_by_frame[frame]['data_index'].append(data_index)
    return data_by_frame


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    defaults_process=DEFAULTS_PROCESS,
    user_id=True,
    output_kwargs=True
)
def poly_line_text_reducer(data_by_frame, **kwargs_dbscan):
    '''
    Reduce the polygon-text answers as a list of lines of text.

    Parameters
    ----------
    data_by_frame : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        * `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_
        * `eps_slope` : How close the angle of two lines need to be in order to be placed in the same angle cluster.
        * `eps_line` : How close vertically two lines need to be in order to be identified as the same line.
        * `eps_word` : How close horizontally the end points of a line need to be in order to be identified as a single point.
        * `gutter_tol` : How much neighboring columns can overlap horizontally and still be identified as multiple columns.
        * `dot_freq` : "line" if dots are drawn at the start and end point of a line, "word" if dots are drawn between each word.
          Note: "word" was proposed for a project but was never used, I don't expect it ever will.  This will likely be depreciated
          in a future release.
        * `min_samples` : For all clustering stages this is how many points need to be close together for a cluster to be identified.
          Set this to 1 for all annotations to be kept
        * `min_word_count` : The minimum number of times a word must be identified for it to be kept in the consensus text.
        * `low_consensus_threshold` : The minimum consensus score allowed to be considered "done"
        * `minimum_views` : A value that is passed along to the font-end to set when lines should turn grey (has no effect on aggregation)

    Returns
    -------
    reduction : dict
        A dictionary with on key for each `frame` of the subject that have lists as values.
        Each item of the list represents one line transcribed of text and is a dictionary
        with these keys:

        * `clusters_x` : the `x` position of each identified word
        * `clusters_y` : the `y` position of each identified word
        * `clusters_text` : A list of text at each cluster position
        * `gutter_label` : A label indicating what "gutter" cluster the line is from
        * `line_slope`: The slope of the line of text in degrees
        * `slope_label` : A label indicating what slope cluster the line is from
        * `number_views` : The number of users that transcribed the line of text
        * `consensus_score` : The average number of users who's text agreed for the line.
          Note, if `consensus_score` is the same a `number_views` every user agreed with each other
        * `low_consensus` : True if the `consensus_score` is less than the threshold set by the
          `low_consensus_threshold` keyword

        For the entire subject the following is also returned:
        * `low_consensus_lines` : The number of lines with low consensus
        * `transcribed_lines` : The total number of lines transcribed on the subject

        Note: the image coordiate system has y increasing downward.
    '''
    user_ids_input = kwargs_dbscan.pop('user_id')
    low_consensus_threshold = kwargs_dbscan.pop('low_consensus_threshold')
    kwargs_cluster = {}
    kwargs_cluster['eps_slope'] = kwargs_dbscan.pop('eps_slope')
    kwargs_cluster['eps_line'] = kwargs_dbscan.pop('eps_line')
    kwargs_cluster['eps_word'] = kwargs_dbscan.pop('eps_word')
    kwargs_cluster['gutter_tol'] = kwargs_dbscan.pop('gutter_tol')
    kwargs_cluster['dot_freq'] = kwargs_dbscan.pop('dot_freq')
    kwargs_cluster['min_word_count'] = kwargs_dbscan.pop('min_word_count')
    _ = kwargs_dbscan.pop('minimum_views')
    return cluster_by_frame(data_by_frame, kwargs_cluster, kwargs_dbscan, user_ids_input, low_consensus_threshold)
