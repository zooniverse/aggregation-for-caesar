'''
Dropdown Extractor
-------------------
This module provides a function to extract dropdown selections from panoptes annotations.
'''
from .extractor_wrapper import extractor_wrapper
from .question_extractor import slugify_or_null
from packaging import version


@extractor_wrapper()
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
    classification_metadata = classification.get('metadata', {})
    classifier_version = version.parse(classification_metadata.get('classifier_version', '1.0'))
    answers = {}
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        answers = {
            'value': []
        }
        if classifier_version < version.parse('2.0'):
            for value in annotation['value']:
                answers['value'].append({slugify_or_null(value['value']): 1})
        elif (annotation.get('taskType', None) == 'dropdown-simple') or (annotation.get('task_type', None) == 'dropdown-simple'):
            key = annotation['value']
            if key is not None:
                if 'selection' in key:
                    key = key['selection']
                elif 'value' in key:
                    key = key['value']
                else:
                    key = None
            answers['value'].append({slugify_or_null(key): 1})
    return answers
