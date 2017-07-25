from collections import OrderedDict
from slugify import slugify
import itertools
from . import question_extractor


def classification_to_extract(classification):
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
                v = question_extractor.classification_to_extract(question_classification)
                extract['answers.{0}'.format(k)] = v
        extract_list.append(extract)
    return extract_list


def survey_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
