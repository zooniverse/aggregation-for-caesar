'''Utility functions used to transform data for filtering'''
import copy
from collections import defaultdict
from ..shape_tools import FEEDBACK_STRATEGIES


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
    '''

    answers = {}

    for key, value in pluck_keys.items():
        key_path = value.strip().split('.')

        try:
            last_value = classification
            for keyi in key_path:
                last_value = last_value[keyi.strip()]
            if(key == 'feedback'):
                feedback_val = get_feedback_info(last_value)
                if feedback_val is not None:
                    answers['feedback'] = feedback_val
            else:
                answers["pluck." + key.strip()] = last_value
        except KeyError:
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

    if not isinstance(feedback_dict, list):
        return None

    if len(feedback_dict) == 0:
        return None

    feedback_data = {}
    feedback_data['success'] = []

    key_list = FEEDBACK_STRATEGIES[feedback_dict[0]['strategy']]

    for key in key_list:
        feedback_data["true_"+key] = []
        #feedback_data["user_"+key] = []

    for classification in feedback_dict:
        feedback_data['success'].append(classification['success'])
        for key in key_list:
            feedback_data["true_"+key].append(classification[key])

            '''
            successfulClassifications = classification['successfulClassifications']
            if len(successfulClassifications) > 0:
                feedback_data["user_"+key].append(successfulClassifications[0][key])
            else:
                feedback_data["user_"+key].append(None)
            '''

    feedback_data['agreement_score'] = sum(feedback_data['success'])/len(feedback_data['success'])
    
    ''' returning feedback_data as list of dicts
    feedback_data = []

    for classification in feedback_dict:
        classi = {}
        classi['success'] = classification['success']
        classi["gold_standard"] = {}
        classi["user_classification"] = {}
        for key in key_list:
            classi['gold_standard'][key] = classification[key]
            if 'successfulClassifications' in classification.keys():
                successfulClassifications = classification['successfulClassifications']
                classi["user_classification"][key] = [sclasses[key] for sclasses in successfulClassifications]
        feedback_data.append(classi)
    ''' 

    return feedback_data
