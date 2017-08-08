from collections import Counter, OrderedDict
from .reducer_wrapper import reducer_wrapper


def process_data(data):
    vote_count = len(data)
    data_out = {}
    for d in data:
        choice = d.pop('choice')
        outer = {}
        for key, value in d.items():
            outer[key] = Counter(value)
        data_out.setdefault(choice, []).append(outer)
    return data_out, vote_count


@reducer_wrapper(process_data=process_data)
def survey_reducer(data_in):
    data, vote_count = data_in
    reduction_list = []
    for choice, answers in data.items():
        reduction = OrderedDict()
        reduction = OrderedDict([
            ('choice', choice),
            ('total_vote_count', vote_count),
            ('choice_count', len(answers))
        ])
        for answer in answers:
            for key, value in answer.items():
                reduction.setdefault(key, Counter())
                reduction[key] += value
        # cast back to dict before returning
        for key, value in reduction.items():
            if isinstance(value, Counter):
                reduction[key] = dict(value)
        reduction_list.append(reduction)
    return reduction_list
