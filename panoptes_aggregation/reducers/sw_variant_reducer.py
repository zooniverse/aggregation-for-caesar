'''
Shakespeares World Variants Reducer
-----------------------------------
This module provides a fuction to reduce the `variants` data from
extracts.
'''
from .reducer_wrapper import reducer_wrapper


@reducer_wrapper()
def sw_variant_reducer(extracts):
    '''Reduce all variants for a subject into one list

    Parameters
    ----------
    extracts : list
        A list of extracts created by
        :meth:`panoptes_aggregation.extractors.sw_variant_extractor.sw_variant_extractor`

    Returns
    -------
    reduction : dict
        A dictionary with at most one key, `variants` with the list of
        all variants in the subject
    '''
    reduction = {}
    variants = []
    for e in extracts:
        if 'variants' in e:
            variants += e['variants']
    if len(variants) > 0:
        reduction['variants'] = variants
    return reduction
