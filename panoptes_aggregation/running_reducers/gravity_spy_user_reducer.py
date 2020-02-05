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
        * `normalized_confusion_matrix`: The column normalized confusion matrix for the user
        * `_store`: The updated store (see above).
    '''
    store = kwargs.pop('store')
    cm = store.get('confusion_matrix', {})
    n = store.get('column_normalization', {})
    user_label = data[0]['user_label']
    gold_label = data[0]['gold_label']
    cm.setdefault(user_label, {}).setdefault(gold_label, 0)
    cm[user_label][gold_label] += 1
    n.setdefault(user_label, 0)
    n[user_label] += 1
    normalized_confusion_matrix = {
        column_key: {
            row_key: row_value / n[column_key] for row_key, row_value in column_value.items()
        } for column_key, column_value in cm.items()
    }
    alpha = {key: value[key] for key, value in normalized_confusion_matrix.items() if key in value}
    alpha_length = len(alpha)
    alpha_min = min(alpha.values())
    return {
        'alpha': alpha,
        'alpha_min': alpha_min,
        'alpha_length': alpha_length,
        'normalized_confusion_matrix': normalized_confusion_matrix,
        '_store': {
            'confusion_matrix': cm,
            'column_normalization': n
        }
    }
