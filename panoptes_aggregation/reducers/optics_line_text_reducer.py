'''
Line Tool with Text Subtask Reducer using OPTICS
------------------------------------------------
This module provides functions to reduce the polygon-text extractions from
:mod:`panoptes_aggregation.extractors.poly_line_text_extractor` using the
density indipended clustering algorithm OPTICS.  It is assumed that all
extracts are full lines of text in the document.
'''
from sklearn.cluster import OPTICS
import numpy as np
from collections import defaultdict
import collatex as col
from .optics_text_utils import get_min_samples, metric, remove_user_duplication, cluster_of_one
from .text_utils import consensus_score, tokenize
from .reducer_wrapper import reducer_wrapper
import warnings

DEFAULTS = {
    'min_samples': {'default': 'auto', 'type': int},
    'max_eps': {'default': np.inf, 'type': float},
    'xi': {'default': 0.05, 'type': float}
}

DEFAULTS_PROCESS = {
    'min_line_length': {'default': 0.0, 'type': float}
}

# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def process_data(data_list, min_line_length=0.0):
    '''Process a list of extractions into a dictinary organized by `frame`

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
        mapping to the data held in `data`.  The first column contains row indicies
        and the second column is an index assigned to each user. `data` is a list of
        dictionaries of the form `{'x': [start_x, end_x], 'y': [start_y, end_y], 'text': ['text for line']}`.
    '''
    data_by_frame = {}
    row_ct = {}
    user_ct = 0
    for user_ct, data in enumerate(data_list):
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {'X': [], 'data': []})
            row_ct.setdefault(frame, 0)
            for x, y, t in zip(value['points']['x'], value['points']['y'], value['text']):
                line_length = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
                if line_length > min_line_length:
                    data_by_frame[frame]['data'].append({
                        'x': [x[0], x[-1]],
                        'y': [y[0], y[-1]],
                        'text': t
                    })
                    data_by_frame[frame]['X'].append([row_ct[frame], user_ct])
                    row_ct[frame] += 1
    return data_by_frame


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS, defaults_process=DEFAULTS_PROCESS)
def optics_line_text_reducer(data_by_frame, **kwargs_optics):
    '''Reduce the line-text extracts as a list of lines of text.

    Parameters
    ----------
    data_by_frame : dict
        A dictionary returned by :meth:`process_data`
    kwargs :
        `See OPTICS <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with on key for each `frame` of the subject that have lists as values.
        Each item of the list represents one line transcribed of text and is a dictionary
        with these keys:

        * `clusters_x` : the `x` position of each identified word
        * `clusters_y` : the `y` position of each identified word
        * `clusters_text` : A list of text at each cluster position
        * `line_slope`: The slope of the line of text in degrees
        * `number_views` : The number of users that transcribed the line of text
        * `consensus_score` : The average number of users who's text agreed for the line
            Note, if `consensus_score` is the same a `number_views` every user agreed with each other

        Note: the image coordiate system is left handed with y increasing downward.
    '''
    output = defaultdict(list)
    min_samples_orig = kwargs_optics.pop('min_samples')
    for frame, value in data_by_frame.items():
        X = np.array(value['X'])
        data = np.array(value['data'])
        num_users = len(np.unique(X[:, 1]))
        if min_samples_orig == 'auto':
            min_samples = get_min_samples(num_users)
        else:
            min_samples = min_samples_orig
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
                    output[frame] += cluster_of_one(X[cdx], data)
                else:
                    xs = [data[int(i)]['x'] for i in X[cdx, 0]]
                    ys = [data[int(i)]['y'] for i in X[cdx, 0]]
                    xm = np.median(xs, axis=0)
                    ym = np.median(ys, axis=0)
                    slope = np.rad2deg(np.arctan2(ym[-1] - ym[0], xm[-1] - xm[0]))
                    collation = col.Collation()
                    witness_keys = []
                    clusters_text = []
                    for i in X[cdx, 0]:
                        text = data[int(i)]['text'][0]
                        if text.strip() != '':
                            key = str(i)
                            witness_keys.append(key)
                            collation.add_plain_witness(key, text)
                    if len(collation.witnesses) > 0:
                        alignment_table = col.collate(collation, near_match=True, segmentation=False)
                        for cols in alignment_table.columns:
                            word_dict = cols.tokens_per_witness
                            word_list = []
                            for key in witness_keys:
                                word_list.append(str(word_dict.get(key, [''])[0]))
                            clusters_text.append(word_list)
                    value = {
                        'clusters_x': xm.tolist(),
                        'clusters_y': ym.tolist(),
                        'clusters_text': clusters_text,
                        'number_views': cdx.sum(),
                        'line_slope': slope,
                        'consensus_score': consensus_score(clusters_text)
                    }
                    output[frame].append(value)
        else:
            # not enough data to cluster so assign each extract
            # to its own cluster
            output[frame] += cluster_of_one(X, data)
    return dict(output)
