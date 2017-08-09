from collections import OrderedDict
from slugify import slugify
import itertools
from .question_extractor import question_extractor
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def survey_extractor(classification):
    extract_list = []
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        extract = OrderedDict()
        choice = slugify(value['choice'], separator='-')
        extract['choice'] = choice
        if 'answers' in value:
            for question, answer in value['answers'].items():
                k = slugify(question, separator='-')
                question_classification = {
                    'annotations': [
                        {'value': answer}
                    ]
                }
                v = question_extractor(question_classification)
                extract['answers_{0}'.format(k)] = v
        extract_list.append(extract)
    return extract_list
