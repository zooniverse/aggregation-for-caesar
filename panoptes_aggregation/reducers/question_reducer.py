from collections import Counter
from .reducer_wrapper import reducer_wrapper

DEFAULTS = {
    'pairs': {'default': False, 'type': bool}
}


def process_data(data, pairs=False):
    data_out = []
    for d in data:
        if pairs:
            new_key = '+'.join(sorted(d))
            data_out.append(Counter({new_key: 1}))
        else:
            data_out.append(Counter(d))
    return data_out


@reducer_wrapper(process_data=process_data, defaults_process=DEFAULTS)
def question_reducer(votes_list):
    counter_total = sum(votes_list, Counter())
    return dict(counter_total)
