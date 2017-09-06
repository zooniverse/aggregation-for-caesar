'''Utility functions used to transform data for tests'''
import copy


def annotation_by_task(classification_in):
    classification = copy.deepcopy(classification_in)
    annotations = classification['annotations']
    ann_by_task = {}
    for annotation in annotations:
        ann_by_task.setdefault(annotation['task'], []).append(annotation)
    classification['annotations'] = list(ann_by_task.values())
    return classification
