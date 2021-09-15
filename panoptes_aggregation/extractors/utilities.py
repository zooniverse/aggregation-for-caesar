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

    pluck_keys : string
        String with a list-like formatting that maps the output key to 
        the location of the value in the classification dict. Must begin
        with a `[` and end with `]`, with each key map separated by a `,`.
        Each entry should be in the form key:location (see examples below).


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
    >>> pluck_keys = '[gold_standard:subject.metadata.is_gold_standard, true_value:subject.metadata.uber_flag_digit]'
    >>> pluck_fields(classification, pluck_keys)
    defaultdict(<class 'list'>, {'gold_standard': 'False', 'true_value': '4'})
    '''
    answers = defaultdict(list)
    pluck_key_list = pluck_keys.replace('[', '').replace(']', '').split(',')
    for entry in pluck_key_list:
        key, value = entry.split(':')
        key_path = value.strip().split('.')

        try:
            last_value = classification
            for keyi in key_path:
                last_value = last_value[keyi.strip()]

            answers["pluck." + key.strip()] = last_value
        except KeyError:
            continue

    return answers
