'''
Text Extractor
--------------
This module provides a function to extract text tasks from panoptes annotations
'''
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper()
def text_extractor(classifiction, **kwargs):
    '''
    Extract annotations from a text task as a string.

    Parameters
    ----------
    classifiction : dict
        A dictionary containing annotations as a key that is a list of panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with one key `text` containing the string for the text entered for the task
    '''
    extract = {}
    if len(classifiction['annotations']) > 0:
        annotaiton = classifiction['annotations'][0]
        extract['text'] = annotaiton['value']
    return extract
