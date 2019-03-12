from .reducer_wrapper import reducer_wrapper
import numpy as np


def process_data(extracts):
    success = []
    for extract in extracts:
        success.append([e['success'] for e in extract])
    return success


@reducer_wrapper(process_data=process_data)
def tess_gold_standard_reducer(data):
    data = np.array(data)
    difficulty = data.sum(axis=0)/len(data)
    output = {
        'difficulty': difficulty.tolist()
    }
    return output
