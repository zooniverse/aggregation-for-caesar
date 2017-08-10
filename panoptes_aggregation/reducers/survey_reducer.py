'''
Survey Reducer
--------------
This module provides functions to reduce survey task extracts from
:mod:`panoptes_aggregation.extractors.survey_extractor`.
'''
from collections import Counter, OrderedDict
from .reducer_wrapper import reducer_wrapper


def process_data(data):
    '''Process a list of extracted survey data into a dictionary of sub-question
    answers sorted organized by `choice`

    Parameters
    ----------
    data : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.survey_extractor.survey_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary where the keys are the `choice` made and the values are a list
        of dicts containing `Counters` for each sub-question asked.
    '''
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
    '''Reduce the survey task answers as a list of dicts (one for each `choice` marked)

    Parameters
    ----------
    data_in : dict
        A dictionary created by :meth:`process_data`

    Returns
    -------
    reduction : list
        A list that has one element for `choice` marked.  Each element is a dict of the form

        * `choice` : The choice made
        * `total_vote_count` : The number of users that classified the subject
        * `choice_count` : The number of users that made this `choice`
        * `answers_*` : Counters for each answer to sub-question `*`
    '''
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
