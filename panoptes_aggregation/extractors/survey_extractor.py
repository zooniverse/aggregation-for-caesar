from collections import OrderedDict
from slugify import slugify
from flatten_json import flatten
import itertools


def classification_to_extract(classification):
    extract = OrderedDict()
    annotation = classification['annotations'][0]
    extract.setdefault('choice', [])
    flat_value = [flatten(v, '.') for v in annotation['value']]
    flat_keys = [list(v.keys()) for v in flat_value]
    keys = set(itertools.chain(*flat_keys))
    answer_keys = [k for k in keys if 'answer' in k]
    for value in flat_value:
        choice = slugify(value['choice'], separator='-')
        extract['choice'].append(choice)
        for answer_key in answer_keys:
            extract.setdefault(answer_key, [])
            if answer_key in value:
                extract[answer_key].append(value[answer_key])
            else:
                extract[answer_key].append('null')
    return extract


def survey_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
