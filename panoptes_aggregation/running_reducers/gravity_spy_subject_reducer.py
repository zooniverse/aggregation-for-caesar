'''
Gravity Spy Subject Reducer
---------------------------
This module porvides functions to calculate subject reducions for the Gravity Spy
project. Extracts are from Ceasars `PluckFieldExtractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper
from collections import Counter


@running_reducer_wrapper(relevant_reduction=True)
def gravity_spy_subject_reducer(data, **kwargs):
    '''Calculate Gravity Spy catagory weights for a subject using volunteer's
    confusion matrices.

    Parameters
    ----------
    data : list
        A list with one item containing the extract with the user's choice and
        the resulting weights from the ML code (stored in the subject metadata)
    store : keyword, dict
        A dictonary with two keys:

        * `number_views`: The number of times the subject has been seen (the ML results count for 1 of these)
        * `catagory_weights_sum`: The running sum for the weights in each catagory
    relevant_reduction : keyword, list
        A list with one item containing the results of the current user's confusion matrix reducer
        (see :meth:`panoptes_aggregation.running_reducers.gravity_spy_user_reduce.gravity_spy_user_reduce`)

    Returns
    -------
    reduction: dict
        A dictonary with four keys:

        * `number_views`: Number of times the subject has been seen (the ML results count for 1 of these)
        * `catagory_weights`: A dictonary of values corrisponding to the probability the subject belongs
            to each listed catagory (all values sum to 1)
        * `max_catagory_weight`: The max value from the `catagory_weights ` dict, used to retire the subject
        * `_store`: The updated store (see above)
    '''
    store = kwargs.pop('store')
    relevant_reduction = kwargs.pop('relevant_reduction')[0]
    user_label = data[0]['user_label']
    try:
        user_weight = Counter(relevant_reduction['data']['normalized_confusion_matrix'][user_label])
    except TypeError:
        # There are no votes on *any* gold standard subjects for this user
        user_weight = Counter({})
    except KeyError:
        # this will happen if the user has never voted for this particular *catagory* on any
        # gold standard subject (i.e. the column of the confusion matrix is all zeros)
        user_weight = Counter({})
    number_views = store.get('number_views', 0)
    if number_views == 0:
        # This is the first time the subject has been viewed.
        # Use the ML weigths as the "first vote"
        number_views += 1
        catagory_weights_sum = Counter(data[0]['ml_weights'])
    else:
        catagory_weights_sum = Counter(store['catagory_weights_sum'])
    if len(user_weight) > 0:
        # Only update values if there is a non-zero weight to add
        number_views += 1
        catagory_weights_sum += user_weight
    catagory_weights = {key: value / number_views for key, value in catagory_weights_sum.items()}
    max_catagory_weight = max(catagory_weights.values())
    return {
        'number_views': number_views,
        'catagory_weights': catagory_weights,
        'max_catagory_weight': max_catagory_weight,
        '_store': {
            'number_views': number_views,
            'catagory_weights_sum': dict(catagory_weights_sum)
        }
    }
