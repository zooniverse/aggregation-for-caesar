def classification_to_extract(classification):
    extract = {}
    for annotation in classification['data']['annotations']:
        for idx, value in enumerate(annotation['value']):
            key_prefix = '{0}_tool{1}_{2}'.format(annotation['task'], value['tool'], idx)
            extract['{0}_x'.format(key_prefix)] = value['x']
            extract['{0}_y'.format(key_prefix)] = value['y']
    return extract


def extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
