from collections import OrderedDict


def classification_to_extract(classification):
    extract = OrderedDict()
    for annotation in classification['annotations']:
        for idx, value in enumerate(annotation['value']):
            key = '{0}_tool{1}'.format(annotation['task'], value['tool'])
            extract.setdefault('{0}_x'.format(key), []).append(value['x'])
            extract.setdefault('{0}_y'.format(key), []).append(value['y'])
    return extract


def extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
