'''
TESS Gold Standard Reducer
--------------------------
This module porvides functions to reduce the gold standard task extracts for the TESS project.
'''
from .reducer_wrapper import reducer_wrapper
import numpy as np


def process_data(extracts):
    '''
    Process the `feedback` extracts

    Parameters
    ----------
    extracts : list
        A list of extracts from Caesar's pluck field extractor

    Returns
    -------
    success : list
        A list-of-lists, one list for each classification with booleans indicating the volunteer's success at
        finding each gold standard transit in a subject.
    '''
    success = []
    for extract in extracts:
        if extract['feedback']:
            success.append([transit['success'] for transit in extract['feedback']])
    return success


@reducer_wrapper(process_data=process_data)
def tess_gold_standard_reducer(data):
    '''
    Calculate the difficulty of a gold standard TESS subject

    Parameters
    ----------
    data : list
        The results of :meth:`process_data`

    Returns
    -------
    output : dict
        A dictinary with one key `difficulty` that is a list with the fraction of volunteers who
        successfully found each gold standard transit in a subject.
    '''
    output = {}
    if len(data) > 0:
        data = np.array(data)
        difficulty = data.sum(axis=0) / len(data)
        output['difficulty'] = difficulty.tolist()
    return output
