from collections import OrderedDict
import copy
import numpy as np
from .extractor_wrapper import extractor_wrapper


def strip_tag(s):
    # remove unicode chars
    return s.encode('ascii', 'ignore').decode('ascii')


@extractor_wrapper
def sw_extractor(classification):
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', []),
        ('slope', [])
    ])
    extract = OrderedDict()
    frame = 'frame0'
    extract[frame] = copy.deepcopy(blank_frame)
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        x = [value['startPoint']['x'], value['endPoint']['x']]
        y = [value['startPoint']['y'], value['endPoint']['y']]
        text = [strip_tag(value['text'])]
        dx = x[-1] - x[0]
        dy = y[-1] - y[0]
        slope = np.rad2deg(np.arctan2(dy, dx))
        extract[frame]['text'].append(text)
        extract[frame]['points']['x'].append(x)
        extract[frame]['points']['y'].append(y)
        extract[frame]['slope'].append(slope)
    return extract
