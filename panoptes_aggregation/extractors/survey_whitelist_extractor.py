"""
Survey Whitelist Extractor
----------------
This module provides a function to extract choices and sub-questions from
panoptes survey tasks, and match those choices against a whitelist in the
subject metadata.
"""

from .survey_extractor import survey_extractor
from .pluck_and_split_extractor import pluck_and_split_extractor
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper()
def survey_whitelist_extractor(classification, **kwargs):
    """Extract annotations from a survey task into a list, matching choices
    against a list plucked from the subject data.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : list
        A list of dicts each with `choice`, `answers`, and `in_whitelist`
        as keys.  Each `choice` made in an annotation is extacted to a
        different element of the list.

    Examples
    --------
    >>> classification = {'annotations': [
            {'value':
                [{'choice': 'AGOUTI', 'answers': {'HOWMANY': '1'}}]
            }
        ]}
    >>> survey_extractor(classification)
    [{'choice': 'agouti','answers_howmany': {'1': 1}, 'in_whitelist': true}]
    """
    whitelist = pluck_and_split_extractor(classification, **kwargs).get("data", [])
    survey = survey_extractor(classification, **kwargs)

    for extract in survey:
        extract["in_whitelist"] = extract.get("choice") in whitelist

    return survey
