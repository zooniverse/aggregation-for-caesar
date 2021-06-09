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
def question_consensus_reducer(data_list, pairs=False, **kwargs):
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
        most_likely = `key` with greatest number of classifications/votes
        num_votes = vote count for mostly likely `key`
        agreement = fraction of total votes held by most likely `key`.
    '''
    answer_list = []
    for data in data_list:
        if pairs:
            answer_list.append('+'.join(sorted(data)))
        else:
            answer_list += list(data)
    counter_total = Counter(answer_list)
    reduced_data = dict(counter_total)
    max_key = max(reduced_data, key=lambda k: reduced_data[k])
    summed_vals = sum(reduced_data.values())
    if reduced_data[max_key] > 0:
        return {
            "most_likely": max_key,
            "num_votes": reduced_data[max_key],
            "agreement": reduced_data[max_key] / summed_vals
        }
    return {
        "num_votes": 0,
    }
