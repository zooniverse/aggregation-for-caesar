'''
Dropdown Reducer
----------------
This module porvides functions to reduce the dropdown task extracts from
:mod:`panoptes_aggregation.extractors.dropdown_extractor`.
'''
from collections import Counter
import numpy as np
from .reducer_wrapper import reducer_wrapper


def process_data(data):
    '''Process a list of extracted dropdown answers into `Counter` objects

    Parameters
    ----------
    data : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.dropdown_extractor.dropdown_extractor`

    Returns
    -------
    process_data : list
        A list-of-lists of `Counter` objects. The is one element of the outer list
        for each classification made, and one element of the inner list for each
        dropdown list in the task.
    '''
    data_out = []
    for extract in data:
        values = []
        for value in extract['value']:
            values.append(Counter(value))
        data_out.append(values)
    return data_out


@reducer_wrapper(process_data=process_data)
def dropdown_reducer(votes_list):
    '''Reducer a list-of-lists of `Counter` objects into one list of dicts

    Parameters
    ----------
    votes_list : list
        A list-of-lists of `Counter` objects from :meth:`process_data`

    Returns
    -------
    reduction : dict
        A dictionary with one key `value` the contains a list of dictionaries
        (one for each dropdown in the task) giving the vote count for each `key`
    '''
    value = np.array(votes_list).sum(axis=0).tolist()
    value = list(map(dict, value))
    output = {
        'value': value
    }
    return output
