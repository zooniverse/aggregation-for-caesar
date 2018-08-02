'''
Dropdown Extractor
-------------------
This module provides a function to extract dropdown selections from panoptes annotations.
'''
from .extractor_wrapper import extractor_wrapper
from .question_extractor import slugify_or_null


@extractor_wrapper
def dropdown_extractor(classification, **kwargs):
    '''Extract annotations from a dropdown task into a Counter object

    Parameters
    ----------
    classification : dict
        A dictionary containing `annotations` as a key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary containing `value` as a key that is a list of
        Counter dictionaries, one entry for each dropdown list in the
        task
    '''
    answers = {}
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        answers = {
            'value': []
        }
        for value in annotation['value']:
            answers['value'].append({slugify_or_null(value['value']): 1})
    return answers
