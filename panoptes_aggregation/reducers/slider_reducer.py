'''
Slider Reducer
--------------
This module porvides functions to reduce the slider task extracts from
:mod:`panoptes_aggregation.extractors.slider_extractor`.
'''
from .reducer_wrapper import reducer_wrapper
import numpy as np


def process_data(data, pairs=False):
    '''Process a list of extracted slider into list

    Parameters
    ----------
    data : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.question_extractor.slider_extractor`

    Returns
    -------
    processed_data : list
        A list of slider values, one for each extraction
    '''
    return [d['slider_value'] for d in data]


@reducer_wrapper(process_data=process_data)
def slider_reducer(votes_list):
    '''Reduce a list of slider values into a mean and median

    Parameters
    ----------
    votes_list : list
        A list of sldier values from :meth:`process_data`

    Returns
    -------
    reduction : dict
        A dictionary giving the mean, median, and variance of the slider values
    '''
    stats = {
        'slider_mean': np.mean(votes_list),
        'slider_median': np.median(votes_list),
        'slider_var': np.var(votes_list)
    }
    return stats
