from collections import Counter
from .process_kwargs import process_kwargs

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


def count_votes(votes_list):
    counter_total = sum(votes_list, Counter())
    return dict(counter_total)


def reducer_request(request):
    kwargs = process_kwargs(request.args, DEFAULTS)
    data = process_data([d['data'] for d in request.get_json()], **kwargs)
    return count_votes(data)


def reducer_base(data_in, **kwargs):
    kwargs_parse = process_kwargs(kwargs, DEFAULTS)
    data = process_data(data_in, **kwargs_parse)
    return count_votes(data)
