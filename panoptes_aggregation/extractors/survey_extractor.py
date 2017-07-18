from collections import OrderedDict
from slugify import slugify


def classification_to_extract(classification):
    extract = OrderedDict()
    annotation = classification['annotations'][0]
    extract.setdefault('choice', [])
    for value in annotation['value']:
        choice = slugify(value['choice'], separator='-')
        extract['choice'].append(choice)
        if 'answers' in value:
            extract.setdefault('answers', {})
            for question, answer in value['answers'].items():
                k = slugify(question, separator='-')
                v = slugify(answer, separator='-')
                extract['answers'].setdefault(k, []).append(v)
    return extract


def survey_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
