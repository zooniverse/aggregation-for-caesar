'''
Line Tool with Text Subtask Reducer using OPTICS
------------------------------------------------
This module provides functions to reduce the polygon-text extractions from
:mod:`panoptes_aggregation.extractors.poly_line_text_extractor` using the
density independent clustering algorithm OPTICS.  It is assumed that all
extracts are full lines of text in the document.
'''
from sklearn.cluster import OPTICS
import numpy as np
from collections import defaultdict
import collatex as col
from .optics_text_utils import get_min_samples, metric, remove_user_duplication, cluster_of_one, order_lines
from .text_utils import consensus_score, tokenize, extractor_index
from .reducer_wrapper import reducer_wrapper
import warnings

DEFAULTS = {
    'min_samples': {'default': 'auto', 'type': int},
    'max_eps': {'default': None, 'type': float},
    'xi': {'default': 0.05, 'type': float},
    'angle_eps': {'default': 30.0, 'type': float},
    'gutter_eps': {'default': 300.0, 'type': float},
    'low_consensus_threshold': {'default': 3.0, 'type': float},
    'minimum_views': {'default': 5, 'type': int}
}

DEFAULTS_PROCESS = {
    'min_line_length': {'default': 0.0, 'type': float}
}

# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def process_data(data_list, min_line_length=0.0):
    '''Process a list of extractions into a dictionary organized by `frame`

    Parameters
    ----------
    data_list : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.poly_line_text_extractor.poly_line_text_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with one key for each frame of the subject. The value for each key
        is a dictionary with two keys `X` and `data`. `X` is a 2D array with each row
        mapping to the data held in `data`.  The first column contains row indices
        and the second column is an index assigned to each user. `data` is a list of
        dictionaries of the form `{'x': [start_x, end_x], 'y': [start_y, end_y],
        'text': ['text for line'], 'gold_standard': bool}`.
    '''
    data_by_frame = {}
    row_ct = {}
    user_ct = 0
    for user_ct, data in enumerate(data_list):
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {'X': [], 'data': []})
            row_ct.setdefault(frame, 0)
            gs = value.get('gold_standard', False)
            for x, y, t in zip(value['points']['x'], value['points']['y'], value['text']):
                line_length = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
                if line_length > min_line_length:
                    data_by_frame[frame]['data'].append({
                        'x': [x[0], x[-1]],
                        'y': [y[0], y[-1]],
                        'text': t,
                        'gold_standard': gs
                    })
                    data_by_frame[frame]['X'].append([row_ct[frame], user_ct])
                    row_ct[frame] += 1
    return data_by_frame


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    defaults_process=DEFAULTS_PROCESS,
    user_id=True,
    output_kwargs=True
)
def optics_line_text_reducer(data_by_frame, **kwargs_optics):
    '''Reduce the line-text extracts as a list of lines of text.

    Parameters
    ----------
    data_by_frame : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        * `See OPTICS <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html>`_
        * `min_samples` : The smallest number of transcribed lines needed to form a cluster.
          `auto` will set this value based on the number of volunteers who transcribed on a page within a subject.
        * `xi` : Determines the minimum steepness on the reachability plot that constitutes a cluster boundary.
        * `angle_eps` : How close the angle of two lines need to be in order to be placed in the same angle cluster.
          Note: This will only change the order of the lines.
        * `gutter_eps` : How close the `x` position of the start of two lines need to be in order to be placed in the same column cluster.
          Note: This will only change the order of the lines.
        * `min_line_length` : The minimum length a transcribed line of text needs to be in order to be used in the reduction.
        * `low_consensus_threshold` : The minimum consensus score allowed to be considered "done".
        * `minimum_views` : A value that is passed along to the font-end to set when lines should turn grey (has no effect on aggregation)

    Returns
    -------
    reduction : dict
        A dictionary with on key for each `frame` of the subject that have lists as values.
        Each item of the list represents one line transcribed of text and is a dictionary
        with these keys:

        * `clusters_x` : the `x` position of each identified word
        * `clusters_y` : the `y` position of each identified word
        * `clusters_text` : A list of lists containing the text at each cluster position
          There is one list for each identified word, and each of those lists contains
          one item for each user that identified the cluster. If the user did not transcribe
          the word an empty string is used.
        * `line_slope`: The slope of the line of text in degrees
        * `number_views` : The number of users that transcribed the line of text
        * `consensus_score` : The average number of users who's text agreed for the line
          Note, if `consensus_score` is the same a `number_views` every user agreed with each other
        * `user_ids`: List of panoptes user ids in the same order as `clusters_text`
        * `gold_standard`: List of bools indicating of the if a transcription was made in frontends
          gold standard mode
        * `slope_label`: integer indicating what slope cluster the line belongs to
        * `gutter_label`: integer indicating what gutter cluster (i.e. column) the line belongs to
        * `low_consensus` : True if the `consensus_score` is less than the threshold set by the
          `low_consensus_threshold` keyword

        For the entire subject the following is also returned:
        * `low_consensus_lines` : The number of lines with low consensus
        * `transcribed_lines` : The total number of lines transcribed on the subject

        Note: the image coordinate system has y increasing downward.
    '''
    user_ids_input = np.array(kwargs_optics.pop('user_id'))
    low_consensus_threshold = kwargs_optics.pop('low_consensus_threshold')
    _ = kwargs_optics.pop('minimum_views')
    output = defaultdict(list)
    min_samples_orig = kwargs_optics.pop('min_samples')
    angle_eps = kwargs_optics.pop('angle_eps')
    gutter_eps = kwargs_optics.pop('gutter_eps')
    max_eps = kwargs_optics.pop('max_eps', np.inf)
    if max_eps is None:
        max_eps = np.inf
    low_consensus_lines = 0
    number_of_lines = 0
    for frame, value in data_by_frame.items():
        frame_unordered = []
        X = np.array(value['X'])
        data = np.array(value['data'])
        if X.size > 0:
            num_users = len(np.unique(X[:, 1]))
            ext_index = np.array(extractor_index(X[:, 1]))
        else:
            num_users = 0
            ext_index = np.array([])
        if min_samples_orig == 'auto':
            min_samples = get_min_samples(num_users)
        else:
            min_samples = max(2, min_samples_orig)
        if num_users >= min_samples:
            db = OPTICS(
                metric=metric,
                metric_params={'data_in': data},
                min_samples=min_samples,
                **kwargs_optics
            )
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=RuntimeWarning)
                db.fit(X)
            clean_labels = remove_user_duplication(
                db.labels_,
                db.core_distances_,
                X[:, 1]
            )
            for label in np.unique(clean_labels):
                cdx = clean_labels == label
                if label == -1:
                    # noise values are assigned to clusters of one
                    frame_unordered += cluster_of_one(X[cdx], data, user_ids_input, ext_index[cdx].tolist())
                else:
                    xs = [data[int(i)]['x'] for i in X[cdx, 0]]
                    ys = [data[int(i)]['y'] for i in X[cdx, 0]]
                    xm = np.median(xs, axis=0)
                    ym = np.median(ys, axis=0)
                    slope = np.rad2deg(np.arctan2(ym[-1] - ym[0], xm[-1] - xm[0]))
                    collation = col.Collation()
                    witness_keys = []
                    clusters_text = []
                    user_ids = []
                    gold_standard = []
                    for row in X[cdx]:
                        index = int(row[0])
                        user_index = int(row[1])
                        text = data[index]['text'][0]
                        gs = data[index]['gold_standard']
                        if text.strip() != '':
                            key = str(index)
                            witness_keys.append(key)
                            user_ids.append(user_ids_input[user_index])
                            gold_standard.append(gs)
                            collation.add_plain_witness(key, text)
                    if len(collation.witnesses) > 0:
                        alignment_table = col.collate(collation, near_match=True, segmentation=False)
                        for cols in alignment_table.columns:
                            word_dict = cols.tokens_per_witness
                            word_list = []
                            for key in witness_keys:
                                word_list.append(str(word_dict.get(key, [''])[0]))
                            clusters_text.append(word_list)
                    consensus_score_value, consensus_text = consensus_score(clusters_text)
                    low_consensus = consensus_score_value < low_consensus_threshold
                    if low_consensus:
                        low_consensus_lines += 1
                    value = {
                        'clusters_x': xm.tolist(),
                        'clusters_y': ym.tolist(),
                        'clusters_text': clusters_text,
                        'number_views': cdx.sum(),
                        'line_slope': slope,
                        'consensus_score': consensus_score_value,
                        'consensus_text': consensus_text,
                        'user_ids': user_ids,
                        'extract_index': ext_index[cdx].tolist(),
                        'gold_standard': gold_standard,
                        'low_consensus': low_consensus,
                        'flagged': low_consensus
                    }
                    number_of_lines += 1
                    frame_unordered.append(value)
        else:
            # not enough data to cluster so assign each extract
            # to its own cluster
            frame_unordered += cluster_of_one(X, data, user_ids_input, ext_index.tolist())
            if len(frame_unordered) > 0:
                low_consensus_lines += 1
                number_of_lines += 1
        output[frame] = order_lines(
            frame_unordered,
            angle_eps=angle_eps,
            gutter_eps=gutter_eps
        )
        output['low_consensus_lines'] = low_consensus_lines
        output['transcribed_lines'] = number_of_lines
        output['reducer'] = 'optics_line_text_reducer'
    return dict(output)
