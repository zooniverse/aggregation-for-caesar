'''
Question Consensus Reducer
--------------------------
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
    '''Reduce a list of extracted questions into a consensus description dict

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
        A dictinary with the following keys

        * `most_likely` : `key` with greatest number of classifications/votes
        * `num_votes` : vote count for mostly likely `key`
        * `agreement` : fraction of total votes held by most likely `key`.

    '''
    # reduce data (similar to question_reducer)
    answer_list = []
    for data in data_list:
        if pairs:
            answer_list.append('+'.join(sorted(data)))
        else:
            answer_list += list(data)
    counter_total = Counter(answer_list)

    # default return value
    result = {
        "num_votes": 0,
    }
    most_common = counter_total.most_common(1)
    # if there exists a most common element (i.e. keys are not empty)
    if len(most_common) > 0 and len(most_common[0]) == 2 and most_common[0][1] > 0:
        max_key = most_common[0][0]
        # sum the values of every key iff there's a max key that has a value > 0
        summed_counts = sum(dict(counter_total).values())
        result = {
            "most_likely": max_key,
            "num_votes": most_common[0][1],
            "agreement": most_common[0][1] / summed_counts
        }
    return result
