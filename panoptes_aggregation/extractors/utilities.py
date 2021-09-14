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
        value given by the corresponding key

    '''
    answers = defaultdict(list)
    pluck_key_list = pluck_keys.replace('[','').replace(']','').split(',')
    for entry in pluck_key_list:
        key, value = entry.split(':')
        key_path = value.strip().split('.')

        try:
            last_value = classification
            for keyi in key_path:
                last_value = last_value[keyi.strip()]

            answers[key.strip()] = last_value
        except KeyError:
            continue

    return answers
