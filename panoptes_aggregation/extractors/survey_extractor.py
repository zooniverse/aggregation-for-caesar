from collections import OrderedDict
from slugify import slugify
from flatten_json import flatten
import itertools


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
                if isinstance(answer, list):
                    v = [slugify(a, separator='-') for a in answer]
                else:
                    v = slugify(answer, separator='-')
                extract['answers.{0}'.format(k)] = v
        extract_list.append(extract)
    return extract_list


def survey_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
