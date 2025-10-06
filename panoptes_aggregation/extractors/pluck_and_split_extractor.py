"""
Pluck and Split Extractor
----------------
This module provides a function to pluck a metadata field and also
split it by a given character.
"""

import jsonpath

from .extractor_wrapper import extractor_wrapper


@extractor_wrapper()
def pluck_and_split_extractor(classification, **kwargs):
    """Pluck fields and split their values by a string.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations, plus classification and subject metadata.

    Returns
    -------
    extraction : dict
        A dictionary containing a list of extracted values.
    """

    matching_values = set()

    for f in jsonpath.findall(kwargs["path"], classification):
        matching_values.update(f.split(kwargs.get("split_str", ",")))

    matching_values = sorted(list(matching_values))
    if len(matching_values) == 0:
        return {}
    if len(matching_values) == 1:
        matching_values = matching_values[0]
    return {"data": matching_values}
