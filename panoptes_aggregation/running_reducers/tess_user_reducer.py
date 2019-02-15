from .running_reducer_wrapper import running_reducer_wrapper
import numpy as np


@running_reducer_wrapper(relevant_reduction=True)
def tess_user_reducer(data, **kwargs):
    data = data[0]['value']
    store = kwargs.pop('store')[0]
    relevant_reduction = kwargs.pop('relevant_reduction')[0]
    number_correct = relevant_reduction['True']
    number_incorrect = relevant_reduction['False']
    d_subject = number_correct / (number_correct + number_incorrect)
    user_correct = sum(data)
    user_incorrect = len(data) - user_correct
    seed_current = (2 * user_correct - user_incorrect) * d_subject
    seed = store.get('seed', 0) + seed_current
    count = store.get('count', 0) + len(data)
    store = {
        'seed': seed,
        'count': count
    }
    c0 = 1
    skill = c0 * pow((1.0 + np.log10(count)), (float(seed)/float(count)))
    skill = min([3.0, max([0.05, skill])])
    return {
        'data': {'skill': skill},
        'store': store
    }
