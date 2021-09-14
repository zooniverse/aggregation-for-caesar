from collections import defaultdict
from slugify import slugify
from .extractor_wrapper import extractor_wrapper
from .utilities import pluck_fields

def slugify_or_null(s):
    '''Slugify value while casting `null` as a string fisrt'''
    if (s is None) or (isinstance(s, bool)) or (isinstance(s, int)):
        return str(s)
    else:
        return slugify(s, separator='-')

@extractor_wrapper()
def pluck_extractor(classification, **kwargs):
    '''Extract annotations from a question task into a Counter object

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary (formated like a counter) indicating what annotations were
        made
    '''

    pluck_keys = kwargs.get('pluck', None)
    
    if pluck_keys is not None:
        return pluck_fields(classification, pluck_keys)

