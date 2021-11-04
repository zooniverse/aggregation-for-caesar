'''Utility functions used to transform data for filtering'''
import copy
import numpy as np
from collections import defaultdict
from ..feedback_strategies import FEEDBACK_STRATEGIES


def annotation_by_task(classification_in):
    classification = copy.deepcopy(classification_in)
    annotations = classification['annotations']
    ann_by_task = defaultdict(list)
    for annotation in annotations:
        ann_by_task[annotation['task']].append(annotation)
    classification['annotations'] = dict(ann_by_task)
    return classification


def pluck_fields(classification, pluck_keys):
    '''
    Main function that is called by the pluck_extractor.
    Functions similarly to the PluckFieldExtractor
    on Caesar, where given a mapping between a key and
    location of the data on the classification JSON,
    this extractor returns a dictionary with each extracted
    value given by the corresponding key.
    Note: passing `feedback` in `pluck_keys` is reserved for
    getting feedback metadata from the FEM's feedback tool. This
    will automatically call `get_feedback_info` which cleans up the
    feedback (subject gold standard) metadata.

    Input
    -----
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    pluck_keys : dict
        Dictionary that maps the output key to
        the location of the value in the classification dict.
        Each entry should be in the form 'key':'location' (see examples below).

    Examples
    --------
    >>> classification = {"id": 359841171, "subject": { \
            "id": 68561182, \
            "metadata": { \
              "filename": "uds_H.gf19767.png", \
              "uber_flag_digit": "4", \
              "is_gold_standard": "False" \
            }, \
        }}
    >>> pluck_keys = {"gold_standard":"subject.metadata.is_gold_standard", "true_value":"subject.metadata.uber_flag_digit"}
    >>> pluck_fields(classification, pluck_keys)
    {'pluck.gold_standard': 'False', 'pluck.true_value': '4'}


    See also
    --------
    get_feedback_info

    '''

    answers = {}

    for key, value in pluck_keys.items():
        key_path = value.strip().split('.')

        # walk down the nested dictionaries in
        # the JSON file until we reach the
        # element we are looking for
        try:
            last_value = classification
            for keyi in key_path:
                last_value = last_value[keyi.strip()]
            # if the key is feedback, we want to process
            # the feedback metadata in the classification
            # and retrieve gold standard data
            if(key == 'feedback'):
                feedback_val = get_feedback_info(last_value)

                # ensure that the classification has feedback data
                if feedback_val is not None:
                    answers['feedback'] = feedback_val
            else:
                # all other keywords use the pluck.[keyname] format
                answers["pluck." + key.strip()] = last_value
        except KeyError:
            # if the requested keyword doesn't exist in the JSON data
            # we ignore it and move on to the next one
            continue

    return answers


def get_feedback_info(feedback_dict):
    '''
    Extracts and processes classification success information from
    the 'feedback' metadata

    Inputs
    ------
    feedback_dict : list
        List of dictionaries, where each entry correspond to
        a feedback metadata in the classification JSON

    Outputs
    -------
    feedback_data : dict
        Dictionary containing information about
        classification success, with the default keys being:
            - 'success': which is a list of boolean success/failure keys
                for each subtask in the classification
            - 'agreement_score': The ratio of successful classifications
                to the total number of subtasks.
        and also the true values depending on the task type
        (see `shape_tools.py`)

    >>> feedback_dict = [{"id":100001,"answer":"3","success":True,"strategy":"singleAnswerQuestion",\
            "failureEnabled":True,"failureMessage":"You got it wrong!",\
            "successEnabled":True,"successMessage":"Congrats!"}]
    >>> get_feedback_info(feedback_dict)
    {'success': [True], 'true_answer': ['3'], 'agreement_score': 1.0}
    '''

    feedback_data = {}

    # each feedback tool has a unique set of keys which
    # hold the gold standard data (see feedback_strategies.py)
    key_list = FEEDBACK_STRATEGIES[feedback_dict[0]['strategy']]

    for classification in feedback_dict:
        # retrieve the success/failure flag for each classification
        # success is True if the volunteer matched the gold standard
        # and False otherwise
        feedback_data.setdefault('success', []).append(classification['success'])
        for key in key_list:
            # also get the true values defined for each subject
            # the keys depend on the type of feedback strategy used in the
            # front end
            feedback_data.setdefault(f"true_{key}", []).append(classification[key])

    # calculate an agreement score for this classification
    # (ratio of successful classifications to number of gold standards)
    feedback_data['agreement_score'] = np.mean(feedback_data['success'])

    return feedback_data
