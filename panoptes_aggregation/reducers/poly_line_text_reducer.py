'''
Polygon As Line Tool for Text Reducer
-------------------------------------
This module provides functions to reduce the polygon-text extractions from
:mod:`panoptes_aggregation.extractors.poly_line_text_extractor`.
'''
import numpy as np
from sklearn.cluster import DBSCAN
from collections import OrderedDict
from .text_utils import gutter, angle_metric, avg_angle
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'eps_slope': {'default': 25.0, 'type': float},
    'eps_line': {'default': 30.0, 'type': float},
    'eps_word': {'default': 25.0, 'type': float},
    'min_samples': {'default': 1, 'type': int},
    'metric': {'default': 'euclidean', 'type': str},
    'algorithm': {'default': 'auto', 'type': str},
    'leaf_size': {'default': 30, 'type': int},
    'p': {'default': None, 'type': float}
}


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
                data_by_frame[frame]['x'].append(x)
                data_by_frame[frame]['y'].append(y)
                data_by_frame[frame]['text'].append(t)
                data_by_frame[frame]['slope'].append(s)
    return data_by_frame


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
def poly_line_text_reducer(data_by_frame, **kwargs):
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
        * `line_slope`: The slope of the line of text in degrees

        Note: the image coordiate system is left handed with y increasing downward.
    '''
    reduced_data = OrderedDict()
    eps_slope = kwargs.pop('eps_slope')
    eps_line = kwargs.pop('eps_line')
    eps_word = kwargs.pop('eps_word')
    metric = kwargs.pop('metric')
    for frame, value in data_by_frame.items():
        reduced_data[frame] = []
        slope_frame = np.array(value['slope']).reshape(-1, 1)
        x_frame = np.array(value['x'])
        y_frame = np.array(value['y'])
        text_frame = np.array(value['text'])
        gutter_labels = gutter(x_frame)
        for gutter_label in set(gutter_labels):
            gdx = gutter_labels == gutter_label
            x = x_frame[gdx]
            y = y_frame[gdx]
            text = text_frame[gdx]
            slope = slope_frame[gdx]
            db_slope = DBSCAN(eps=eps_slope, metric=angle_metric, **kwargs).fit(slope)
            for slope_label in set(db_slope.labels_):
                if slope_label > -1:
                    sdx = db_slope.labels_ == slope_label
                    xy_slope = np.array(list(zip(np.hstack(x[sdx]), np.hstack(y[sdx]))))
                    text_slope = np.hstack(text[sdx])
                    avg_slope = avg_angle(slope[sdx])
                    c = np.cos(np.deg2rad(-avg_slope))
                    s = np.sin(np.deg2rad(-avg_slope))
                    R = np.array([[c, -s], [s, c]])
                    xy_rotate = np.dot(xy_slope, R.T)
                    lines = xy_rotate[:, 1].reshape(-1, 1)
                    words = xy_rotate[:, 0].reshape(-1, 1)
                    db_lines = DBSCAN(eps=eps_line, metric=metric, **kwargs).fit(lines)
                    for line_label in set(db_lines.labels_):
                        if line_label > -1:
                            line_dict = {
                                'clusters_x': [],
                                'clusters_y': [],
                                'clusters_text': [],
                                'line_slope': avg_slope
                            }
                            ldx = db_lines.labels_ == line_label
                            text_line = text_slope[ldx]
                            xy_line = xy_slope[ldx]
                            words_line = words[ldx]
                            db_words = DBSCAN(eps=eps_word, metric=metric, **kwargs).fit(words_line)
                            for word_label in set(db_words.labels_):
                                if word_label > -1:
                                    wdx = db_words.labels_ == word_label
                                    word_x, word_y = xy_line[wdx].mean(axis=0)
                                    line_dict['clusters_x'].append(word_x)
                                    line_dict['clusters_y'].append(word_y)
                                    line_dict['clusters_text'].append(list(text_line[wdx]))
                            reduced_data[frame].append(line_dict)
    return reduced_data
