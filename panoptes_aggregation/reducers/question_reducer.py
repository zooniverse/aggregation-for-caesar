'''
Question Reducer
----------------
This module provides functions to reduce the question task extracts from
:mod:`panoptes_aggregation.extractors.question_extractor`.
'''
from collections import defaultdict
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'pairs': {'default': False, 'type': bool},
    'track_user_ids': {'default': False, 'type': bool}
}


@reducer_wrapper(defaults_data=DEFAULTS, user_id=True)
def question_reducer(data_list, pairs=False, track_user_ids=False, **kwargs):
    '''Reduce a list of extracted questions into a "counter" dict

    Parameters
    ----------
    data_list : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.question_extractor.question_extractor`
    pairs : bool, optional
        Default `False`. How multiple choice questions are treated.
        When `True` the set of all choices is treated as a single answer
    track_user_ids : bool, optional
        Default `False`. Set to `True` to also track the user_ids that gave
        each answer.

    Returns
    -------
    reduction : dict
        A dictionary (formated as a `Counter`) giving the vote count for each
        `key`. If `user_ids` is `True` it will also contain a list of user_ids
        for each answer given.
    '''
    user_id_list = kwargs.pop('user_id')
    result = defaultdict(int)
    for data, user_id in zip(data_list, user_id_list):
        if pairs:
            key = '+'.join(sorted(data))
            result[key] += 1
            if track_user_ids:
                key_user_ids = f'user_ids_{key}'
                result.setdefault(key_user_ids, []).append(user_id)
        else:
            for key in data:
                result[key] += 1
                if track_user_ids:
                    key_user_ids = f'user_ids_{key}'
                    result.setdefault(key_user_ids, []).append(user_id)
    return dict(result)
