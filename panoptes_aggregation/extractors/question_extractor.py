'''
Question Extractor
------------------
This module provides a function to extract question tasks (single and multiple)
from panoptes annotations.
'''
from collections import Counter
from slugify import slugify
from .extractor_wrapper import extractor_wrapper


def slugify_or_null(s):
    '''Slugify value while casting `null` as a string fisrt'''
    if (s is None) or (isinstance(s, bool)) or (isinstance(s, int)):
        return str(s)
    else:
        return slugify(s, separator='-')


@extractor_wrapper
def question_extractor(classification, **kwargs):
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

    Examples
    --------
    >>> classification_multiple = {'annotations': [
        {
            'vlaue': ['Blue', 'Green']
        }
    ]}
    >>> question_extractor(classification_multiple)
    {'blue': 1, 'green': 1}

    >>> classification_single = {'annotations': [
        {'vlaue': 'Yes'}
    ]}
    >>> question_extractor(classification_single)
    {'yes': 1}
    '''
    #: assumes only one task is filtered into the extractor
    answers = Counter()
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        if isinstance(annotation['value'], list):
            for answer in annotation['value']:
                answers[slugify_or_null(answer)] += 1
        else:
            answers[slugify_or_null(annotation['value'])] += 1
    return dict(answers)
