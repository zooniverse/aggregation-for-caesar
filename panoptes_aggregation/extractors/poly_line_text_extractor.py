from collections import OrderedDict
import copy


def classification_to_extract(classification):
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', [])
    ])
    extract = OrderedDict()
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        frame = 'frame{0}'.format(value['frame'])
        extract.setdefault(frame, copy.deepcopy(blank_frame))
        text = value['details'][0]['value']
        words = text.split(' ')
        # NOTE: if `words` and `points` are differnt lengths
        # the extract will only contain the *shorter* of the
        # two lists (assuming they match from the front)
        for word, point in zip(words, value['points']):
            extract[frame]['text'].append(word)
            extract[frame]['points']['x'].append(point['x'])
            extract[frame]['points']['y'].append(point['y'])
    return extract


def poly_line_text_extractor_request(request):
    data = request.get_json()
    return classification_to_extract(data)
