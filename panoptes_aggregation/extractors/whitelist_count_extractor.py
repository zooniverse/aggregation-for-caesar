"""
Survey Whitelist Extractor
----------------
This module provides a function to extract choices and sub-questions from
panoptes survey tasks, and match those choices against a whitelist in the
subject metadata.
"""

from .pluck_and_split_extractor import pluck_and_split_extractor
from .extractor_wrapper import extractor_wrapper
from slugify import slugify


@extractor_wrapper()
def whitelist_count_extractor(classification, **kwargs):
    """Extract whether survey choices match a subject metadata whitelist.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dict shaped like a question extraction, suitable for reduction with
        the question reducer. If any selected survey choice is in the
        whitelist, the dict contains ``in_whitelist``. If any selected survey
        choice is not in the whitelist, the dict contains ``not_in_whitelist``.

    Examples
    --------
    >>> classification = {'annotations': [
            {'value':
                [{'choice': 'AGOUTI', 'answers': {'HOWMANY': '1'}}]
            }
        ]}
    >>> whitelist_count_extractor(classification)
    {'in_whitelist': 1}
    """
    # We are already inside extractor_wrapper here, so annotations have been
    # normalized to a plain list. Call the underlying extractor functions
    # directly to avoid re-wrapping that normalized payload.
    whitelist = pluck_and_split_extractor._original(classification, **kwargs).get("data", [])
    if isinstance(whitelist, str):
        whitelist = [whitelist]
    whitelist = {slugify(choice.strip(), separator="-") for choice in whitelist}

    extraction = {}
    if len(classification["annotations"]) > 0:
        annotation = classification["annotations"][0]
        for value in annotation["value"]:
            choice = slugify(value["choice"], separator="-")
            if choice in whitelist:
                extraction["in_whitelist"] = 1
            else:
                extraction["not_in_whitelist"] = 1

    return extraction
