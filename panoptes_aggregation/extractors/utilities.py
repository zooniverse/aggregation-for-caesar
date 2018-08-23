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
