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


@reducer_wrapper(defaults_data=DEFAULTS)
def question_reducer(data_list, pairs=False, **kwargs):
    '''Reduce a list of extracted questions into a "counter" dict

    Parameters
    ----------
    data_list : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.question_extractor.question_extractor`
    pairs : bool, optional
        Default `False`. How multiple choice questions are treated.
        When `True` the set of all choices is treated as a single answer

    Returns
    -------
    reduction : dict
        A dictionary (formated as a `Counter`) giving the vote count for each
        `key`
    '''
    answer_list = []
    for data in data_list:
        if pairs:
            answer_list.append('+'.join(sorted(data)))
        else:
            answer_list += list(data)
    counter_total = Counter(answer_list)
    return dict(counter_total)
