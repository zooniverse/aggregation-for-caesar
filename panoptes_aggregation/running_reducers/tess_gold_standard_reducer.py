'''
TESS Gold Standard Running Reducer
----------------------------------
This module porvides functions to reduce the gold standard task extracts for the TESS project in running mode.
'''
from ..reducers.tess_gold_standard_reducer import process_data as tgsr_process_data
from .running_reducer_wrapper import running_reducer_wrapper
import numpy as np


@running_reducer_wrapper()
def tess_gold_standard_reducer_rr(data, **kwargs):
    '''
    See :meth:`panoptes_aggregation.reducers.tess_gold_standard_reducer.tess_gold_standard_reducer`
    '''
    store = kwargs.pop('store')
    output = {
        '_store': store
    }
    count = store.get('count', 0)
    processed_data = tgsr_process_data(data)
    if len(processed_data) > 0:
        current_successes = np.array(processed_data[0], dtype=int)
        past_successes = np.array(
            store.get(
                'number_of_successes',
                np.zeros(len(current_successes), dtype=int)
            )
        )
        count += 1
        number_of_successes = past_successes + current_successes
        output['difficulty'] = (number_of_successes / count).tolist()
        output['_store'] = {
            'number_of_successes': number_of_successes.tolist(),
            'count': count
        }
    elif count > 0:
        past_successes = np.array(store['number_of_successes'])
        output['difficulty'] = (past_successes / count).tolist()
    return output
