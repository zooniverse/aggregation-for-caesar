'''
Shakespeares World Variants Extractor
-------------------------------------
This module provides a fuction to extract the `variants` data from
annotations made on Shakespeares World.
'''
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def sw_variant_extractor(classification, **kwargs):
    '''Extract all variants in a classification into one list

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        Shakespeares World annotations

    Returns
    -------
    extraction : dict
        A dictionary with at most one key, `variants` with the list of
        all variants in the classification
    '''
    extract = {}
    variants = []
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        for value in annotation['value']:
            if 'variants' in value:
                variants += list(filter(None, value['variants']))
        if len(variants) > 0:
            extract['variants'] = variants
    return extract
