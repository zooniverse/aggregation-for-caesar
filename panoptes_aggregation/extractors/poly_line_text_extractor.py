from collections import OrderedDict


def classification_to_extract(classification):
    extract = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', []),
        ('frame', [])
    ])
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        text = value['details'][0]['value']
        words = text.split(' ')
        for word, point in zip(words, value['points']):
            extract['frame'].append(value['frame'])
            extract['text'].append(word)
            extract['points']['x'].append(point['x'])
            extract['points']['y'].append(point['y'])
    return extract


def poly_line_text_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
