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
from .optics_text_utils import *
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'min_samples': {'default': 'auto', 'type': int},
    'max_eps': {'default': np.inf, 'type': float},
    'xi': {'default': 0.05, 'type': float},
}


def process_data(data_list):
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
        dictionaries of the form {`x`: [start_x, end_x], `y`: [start_y, end_y], 'text': ['text for line']}.
    '''
    data_by_frame = {}
    row_ct = {}
    user_ct = 0
    for user_ct, data in enumerate(data_list):
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {'X': [], 'data': []})
            row_ct.setdefault(frame, 0)
            for x, y, t in zip(value['points']['x'], value['points']['y'], value['text']):
                data_by_frame[frame]['data'].append({
                    'x': [x[0], x[-1]],
                    'y': [y[0], y[-1]],
                    'text': t
                })
                data_by_frame[frame]['X'].append([row_ct[frame], user_ct])
                row_ct[frame] += 1
    return data_by_frame


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
def optics_line_text_reducer(data_by_frame, **kwargs_optics):
    return {'value': 'tmp'}
