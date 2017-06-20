from collections import Counter
from slugify import slugify


def classification_to_extract(classification):
    # assumes only one task is filtered into the extractor
    annotation = classification['annotations'][0]
    task_key = annotation['task']
    answers = Counter()
    if isinstance(annotation['value'], list):
        for answer in annotation['value']:
            answers[slugify(answer, separator='-')] += 1
    else:
        answers[slugify(annotation['value'], separator='-')] += 1
    return dict(answers)


def extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
