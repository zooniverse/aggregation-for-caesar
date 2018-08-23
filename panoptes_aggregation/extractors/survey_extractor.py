'''
Survey Extractor
----------------
This module provides a function to extract choices and sub-questions from
panoptes survey tasks.
'''
from collections import OrderedDict
from slugify import slugify
from .question_extractor import question_extractor
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def survey_extractor(classification, **kwargs):
    '''Extract annotations from a survye task into a list

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : list
        A list of dicts each with `choice` and `answers` as keys.  Each
        `choice` made in an annotation is extacted to a different element
        of the list.

    Examples
    --------
    >>> classification = {'annotations': [
            {'value':
                [{'choice': 'AGOUTI', 'answers': {'HOWMANY': '1'}}]
            }
        ]}
    >>> survey_extractor(classification)
    [{'choice': 'agouti','answers_howmany': {'1': 1}}]
    '''
    extract_list = []
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        for value in annotation['value']:
            extract = OrderedDict()
            choice = slugify(value['choice'], separator='-')
            extract['choice'] = choice
            if 'answers' in value:
                for question, answer in value['answers'].items():
                    k = slugify(question, separator='-')
                    question_classification = {
                        'annotations': {
                            'ST': [
                                {'value': answer}
                            ]
                        }
                    }
                    v = question_extractor(question_classification, no_version=True)
                    extract['answers_{0}'.format(k)] = v
            extract_list.append(extract)
    return extract_list
