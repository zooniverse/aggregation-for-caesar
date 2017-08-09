from collections import Counter
from slugify import slugify
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def question_extractor(classification):
    # assumes only one task is filtered into the extractor
    annotation = classification['annotations'][0]
    answers = Counter()
    if isinstance(annotation['value'], list):
        for answer in annotation['value']:
            answers[slugify(answer, separator='-')] += 1
    else:
        answers[slugify(annotation['value'], separator='-')] += 1
    return dict(answers)
