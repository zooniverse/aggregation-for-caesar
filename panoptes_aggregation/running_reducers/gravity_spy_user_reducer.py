'''
Gravity Spy User Reducer
------------------------
This module porvides functions to calculate uesr weights for the Gravity Spy
project. Extracts are from Ceasars `PluckFieldExtractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper


@running_reducer_wrapper()
def gravity_spy_user_reducer(data, **kwargs):
    '''Calculate Gravity Spy user weights based on a confusion matrix
    from gold standard data.

    Parameters
    ----------
    data : list
        A list with one item containing the extract with the user's choice
        and the gold standard label.
    store : keyword, list
        A dictonary with two keys:

        * `confusion_matrix`: The confusion matrix for the user (stored as nested dict).
            The frist key is the choice given by the user, the second key is the gold
            standard label.
        * `column_normalization`: The sum of each of the columns (used for normaliztion).
            i.e. The total number of time the user has vote for each choice.
    
    Returns
    -------
    reduction : dict
        A dictionary with four keys:

        * `alpha`: A dictionary of values indicating how well the user classifies each 
            catagory they have seen gold standard images for (diagonal of the normalized
            confusion matrix).
        * `alpha_min`: The minimum value of `alpha`, this is used to determin when a user
            should be promoted.
        * `alpha_length`: The number of values in the `alpha` dict, used to make sure the
            user has seen every gold standard class of a level before being promoted
        * `_store`: The updated store (see above).
    '''
    store = kwargs.pop('store')
    store.setdefault('confusion_matrix', {})
    store.setdefault('column_normalization', {})
    user_label = data[0]['user_label']
    gold_label = data[0]['gold_label']
    store['confusion_matrix'].setdefault(user_label, {}).setdefault(gold_label, 0)
    store['confusion_matrix'][user_label][gold_label] += 1
    store['column_normalization'].setdefault(user_label, 0)
    store['column_normalization'][user_label] += 1
    alpha = {}
    for column_key, norm_value in store['column_normalization'].items():
        cm_value = store['confusion_matrix'][column_key].get(column_key, 0)
        if cm_value > 0:
            alpha[column_key] = cm_value / norm_value
    alpha_length = len(alpha)
    alpha_min = min(alpha.values())
    return {
        'alpha': alpha,
        'alpha_min': alpha_min,
        'alpha_length': alpha_length,
        '_store': store
    }
