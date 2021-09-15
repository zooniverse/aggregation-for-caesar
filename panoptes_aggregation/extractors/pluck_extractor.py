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
def pluck_extractor(classification, pluck, **kwargs):
    '''Extract annotations from a question task into a Counter object

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with the entries defined by the `pluck` argument

    See also
    --------
    .utilities.pluck_fields

    '''
    if pluck is not None:
        return pluck_fields(classification, pluck)
