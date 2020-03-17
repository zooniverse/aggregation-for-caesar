'''
Text Extractor
--------------
This module provides a function to extract text tasks from panoptes annotations
'''
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper(gold_standard=True)
def text_extractor(classification, gold_standard=False, **kwargs):
    '''
    Extract annotations from a text task as a string.

    Parameters
    ----------
    classification : dict
        A dictionary containing annotations as a key that is a list of panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with two keys
        * `text`: the string for the text entered for the task
        * `gold_standard`: bool indicated if the classification was made in gold standard mode
    '''
    extract = {}
    if len(classification['annotations']) > 0:
        annotaiton = classification['annotations'][0]
        extract['text'] = annotaiton['value']
        extract['gold_standard'] = gold_standard
    return extract
