'''
Text Extractor
--------------
This module provides a function to extract text tasks from panoptes annotations
'''
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper()
def text_extractor(classifiction, **kwargs):
    extract = {}
    if len(classifiction['annotations']) > 0:
        annotaiton = classifiction['annotations'][0]
        extract['text'] = annotaiton['value']
    return extract
