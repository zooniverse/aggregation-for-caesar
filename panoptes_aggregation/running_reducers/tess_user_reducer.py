'''
TESS User Reducer
-----------------
This module porvides functions to calculate uesr weights for the TESS project.
Extracts are from Ceasars `PluckFieldExtractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper
import numpy as np


@running_reducer_wrapper(relevant_reduction=True)
def tess_user_reducer(data, **kwargs):
    '''Calculate TESS user weights

    Parameters
    ----------
    data : list
        A list with one item containing the extract with the user's feedback on a
        gold standard subject
    store : keyword, list
        A list with one item containing the user's current store.  This item is a
        dictinary with two keys:

        * `seed`: sum of all previous `seed` values
        * `count`: sum of all previous gold standard transits seen
    relevant_reduction : keyword, list
        A list with one item containing the results of the current subject's stats reducer.
        This item is a dictinary with two keys:

        * `True`: number of users who correctly identified the gold standard transits in the subject
        * `False`: number of users who incorrectly identified the gold standard transits in the subject

    Returns
    -------
    reduction : dict
        A dictinary with two keys:

        * `data`: A dictionary with the `skill` value as the only item
        * `store`: The updated store for the user
    '''
    success = [d['success'] for d in data[0]['feedback']]
    store = kwargs.pop('store')
    relevant_reduction = kwargs.pop('relevant_reduction')[0]
    try:
        d_subject = relevant_reduction['data']['difficulty']
    except:
        d_subject = 0

    seed_current = (np.where(success, 2, -1) * d_subject).sum()
    seed = store.get('seed', 0) + seed_current
    count = store.get('count', 0) + len(success)
    store = {
        'seed': seed,
        'count': count
    }
    c0 = 1
    skill = c0 * pow((1.0 + np.log10(count)), (seed / count))
    skill = min([3.0, max([0.05, skill])])
    return {
        'skill': skill,
        '_store': store
    }
