'''
Gravity Spy Subject Reducer
---------------------------
This module provides functions to calculate subject reductions for the Gravity Spy
project. Extracts are from caesar's `PluckFieldExtractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper
from collections import Counter

DEFAULTS = {
    'none_key': {'default': 'NONEOFTHEABOVE', 'type': str}
}


@running_reducer_wrapper(relevant_reduction=True, defaults_data=DEFAULTS)
def gravity_spy_subject_reducer(data, none_key="NONEOFTHEABOVE", **kwargs):
    '''Calculate Gravity Spy category weights for a subject using volunteer's
    confusion matrices.

    Parameters
    ----------
    data : list
        A list with one item containing the extract with the user's choice and
        the resulting weights from the ML code (stored in the subject metadata)
    none_key : string
        The key used for a "none of the above" answer
    store : keyword, dict
        A dictionary with two keys:

        * `number_views`: The number of times the subject has been seen (the ML results count for 1 of these)
        * `category_weights_sum`: The running sum for the weights in each category

    relevant_reduction : keyword, list
        A list with one item containing the results of the current user's confusion matrix reducer
        (see :meth:`panoptes_aggregation.running_reducers.gravity_spy_user_reduce.gravity_spy_user_reduce`)

    Returns
    -------
    reduction: dict
        A dictionary with the following keys:

        * `number_views`: Number of times the subject has been seen (the ML results count for 1 of these)
        * `category_weights`: A dictionary of values corresponding to the probability the subject belongs
          to each listed category (all values sum to 1)
        * `max_category_weight`: The max value from the `category_weights` dict, used to retire the subject
        * `_store` : The updated store (see above)

    '''
    store = kwargs.pop('store')
    relevant_reduction = kwargs.pop('relevant_reduction')[0]
    user_label = data[0]['user_label']
    none_of_the_above_count = store.get('none_of_the_above_count', 0)
    if user_label == none_key:
        none_of_the_above_count += 1
        user_weight = Counter({})
    else:
        try:
            user_weight = Counter(relevant_reduction['data']['normalized_confusion_matrix'][user_label])
        except TypeError:
            # There are no votes on *any* gold standard subjects for this user
            user_weight = Counter({})
        except KeyError:
            # this will happen if the user has never voted for this particular *category* on any
            # gold standard subject (i.e. the column of the confusion matrix is all zeros)
            user_weight = Counter({})
    number_views = store.get('number_views', 0)
    if number_views == 0:
        # This is the first time the subject has been viewed.
        # Use the ML weights as the "first vote"
        number_views += 1
        category_weights_sum = Counter(data[0]['ml_weights'])
    else:
        category_weights_sum = Counter(store['category_weights_sum'])
    if len(user_weight) > 0:
        # Only update values if there is a non-zero weight to add
        number_views += 1
        category_weights_sum += user_weight
    category_weights = {key: value / number_views for key, value in category_weights_sum.items()}
    max_category_weight = max(category_weights.values())
    return {
        'number_views': number_views,
        'none_of_the_above_count': none_of_the_above_count,
        'category_weights': category_weights,
        'max_category_weight': max_category_weight,
        '_store': {
            'number_views': number_views,
            'none_of_the_above_count': none_of_the_above_count,
            'category_weights_sum': dict(category_weights_sum)
        }
    }
