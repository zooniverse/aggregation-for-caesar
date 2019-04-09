from .reducer_wrapper import reducer_wrapper
import numpy as np


def process_data(extracts):
    success = []
    for extract in extracts:
        if extract['feedback']:
            success.append([transit['success'] for transit in extract['feedback']])
    return success


@reducer_wrapper(process_data=process_data)
def tess_gold_standard_reducer(data):
    output = {}
    if len(data) > 0:
        data = np.array(data)
        difficulty = data.sum(axis=0) / len(data)
        output['difficulty'] = difficulty.tolist()
    return output
