import copy
from .extractor_wrapper import extractor_wrapper
from collections import OrderedDict


@extractor_wrapper
def sw_graphic_extractor(classification):
    blank_frame = OrderedDict([
        ('tool0_x', []),
        ('tool0_y', []),
        ('tool0_width', []),
        ('tool0_height', [])
    ])
    extract = OrderedDict()
    frame = 'frame0'
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        if ('type' in value) and ((value['type'] == 'graphic') or (value['type'] == 'image')):
            extract.setdefault(frame, copy.deepcopy(blank_frame))
            if (value['type'] == 'graphic'):
                extract[frame].setdefault('tool0_tag', []).append(value['tag'])
            extract[frame]['tool0_x'].append(value['x'])
            extract[frame]['tool0_y'].append(value['y'])
            extract[frame]['tool0_width'].append(value['width'])
            extract[frame]['tool0_height'].append(value['height'])
    return extract
