'''Utility functions used to transform data for filtering'''
import copy
from collections import defaultdict


def annotation_by_task(classification_in):
    classification = copy.deepcopy(classification_in)
    annotations = classification['annotations']
    ann_by_task = defaultdict(list)
    for annotation in annotations:
        ann_by_task[annotation['task']].append(annotation)
    classification['annotations'] = dict(ann_by_task)
    return classification

<<<<<<< HEAD

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
=======
def pluck_fields(classification, pluck_keys):
    '''
        Main function that is called by the pluck_extractor. 
        Functions similarly to the PluckFieldExtractor
        on Caesar, where given a mapping between a key and
        location of the data on the classification JSON,
        this extractor returns a dictionary with each extracted
        value given by the corresponding key

    '''
    answers = defaultdict(list)
    pluck_key_list = pluck_keys.replace('[','').replace(']','').split(',')
    for entry in pluck_key_list:
        key, value = entry.split(':')
>>>>>>> 4c48fd4 (added pluck field extractor)
        key_path = value.strip().split('.')

        try:
            last_value = classification
            for keyi in key_path:
                last_value = last_value[keyi.strip()]

<<<<<<< HEAD
            answers["pluck." + key.strip()] = last_value
=======
            answers[key.strip()] = last_value
>>>>>>> 4c48fd4 (added pluck field extractor)
        except KeyError:
            continue

    return answers
