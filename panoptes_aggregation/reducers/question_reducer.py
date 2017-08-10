'''
Question Reducer
----------------
This module porvides functions to reduce the question task extracts from
:mod:`panoptes_aggregation.extractors.question_extractor`.
'''
from collections import Counter
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'pairs': {'default': False, 'type': bool}
}


def process_data(data, pairs=False):
    '''Process a list of extracted questions into `Counter` objects

    Parameters
    ----------
    data : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.question_extractor.question_extractor`
    pairs : bool, optional
        Default `False`. How multiple choice questions are treated.
        When `True` the set of all choices is treated as a single answer

    Returns
    -------
    processed_data : list
        A list of `Counter` objects, one for each extraction
    '''
    data_out = []
    for d in data:
        if pairs:
            new_key = '+'.join(sorted(d))
            data_out.append(Counter({new_key: 1}))
        else:
            data_out.append(Counter(d))
    return data_out


@reducer_wrapper(process_data=process_data, defaults_process=DEFAULTS)
def question_reducer(votes_list):
    '''Reduce a list of `Counter` objects into a single dict

    Parameters
    ----------
    votes_list : list
        A list of `Counter` objects from :meth:`process_data`

    Returns
    -------
    reduction : dict
        A dictionary (formated as a `Counter`) giving the vote count for each
        `key`
    '''
    counter_total = sum(votes_list, Counter())
    return dict(counter_total)
