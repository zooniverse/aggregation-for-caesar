'''
Slider Extractor
----------------
This module provides a function to extract slider tasks from panoptes annotations.
'''
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def slider_extractor(classification, **kwargs):
    '''Extract annotations from a slider task

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary indicating what annotation was made
    '''
    #: assumes only one task is filtered into the extractor
    answers = {}
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        answers['slider_value'] = annotation['value']
    return answers
