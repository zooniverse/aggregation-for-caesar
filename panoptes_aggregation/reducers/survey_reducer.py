from collections import Counter, OrderedDict


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


def count_votes(data, vote_count=0):
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


def survey_reducer_request(request):
    data, vote_count = process_data([d['data'] for d in request.get_json()])
    return count_votes(data, vote_count=vote_count)


def reducer_base(data_in):
    data, vote_count = process_data(data_in)
    return count_votes(data, vote_count=vote_count)
