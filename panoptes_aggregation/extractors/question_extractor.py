'''This module provides function to extract question tasks (single and multiple)
from panoptes annotations.
'''
from collections import Counter
from slugify import slugify
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def question_extractor(classification):
    r'''Extact annotations from a question task into a Counter object

    Parameters
    ----------
    classification : dict
                    A dictionary containing a `annotations` key that is a list of
                    panoptes annotations

    Returns
    -------
    dict
        A dictionary in the formation of a counter indicating what annotations were
        made

    Examples
    --------
    >>> classification_multiple = {'annotations': [{'vlaue': ['Blue', 'Green']}]}
    >>> classification_to_extract(classification_multiple)
    {'blue': 1, 'green': 1}
    >>> classification_single = {'annotations': [{'vlaue': 'Yes'}]}
    >>> classification_to_extract(classification_single)
    {'yes': 1}
    '''
    # assumes only one task is filtered into the extractor
    annotation = classification['annotations'][0]
    answers = Counter()
    if isinstance(annotation['value'], list):
        for answer in annotation['value']:
            answers[slugify(answer, separator='-')] += 1
    else:
        answers[slugify(annotation['value'], separator='-')] += 1
    return dict(answers)
