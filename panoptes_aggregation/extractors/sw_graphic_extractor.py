from .extractor_wrapper import extractor_wrapper
from collections import OrderedDict


def exist_and_finite(d, key):
    return (key in d) and (d[key] != 'NaN')


@extractor_wrapper
def sw_graphic_extractor(classification):
    extract = OrderedDict()
    frame = 'frame0'
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        for value in annotation['value']:
            if ('type' in value) and ((value['type'] == 'graphic') or (value['type'] == 'image')):
                exist = exist_and_finite(value, 'x') and exist_and_finite(value, 'y') and exist_and_finite(value, 'width') and exist_and_finite(value, 'height')
                if (value['type'] == 'graphic'):
                    exist = exist and exist_and_finite(value, 'tag')
                    if exist:
                        extract.setdefault(frame, OrderedDict())
                        extract[frame].setdefault('tool0_tag', []).append(value['tag'])
                if exist:
                    extract.setdefault(frame, OrderedDict())
                    extract[frame].setdefault('tool0_x', []).append(float(value['x']))
                    extract[frame].setdefault('tool0_y', []).append(float(value['y']))
                    extract[frame].setdefault('tool0_width', []).append(float(value['width']))
                    extract[frame].setdefault('tool0_height', []).append(float(value['height']))
    return extract
