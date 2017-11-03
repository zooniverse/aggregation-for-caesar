'''
Rectangle Extractor
-------------------
This module provides a function to extract drawn rectangles from panoptes annotations.
'''
from collections import OrderedDict
import copy
from slugify import slugify
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def rectangle_extractor(classification):
    extract = OrderedDict()
    blank_frame = OrderedDict([
        ('x', []),
        ('y', []),
        ('width', []),
        ('height', [])
    ])
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for idx, value in enumerate(annotation['value']):
            key = '{0}_tool{1}'.format(task_key, value['tool'])
            frame = 'frame{0}'.format(value['frame'])
            if ('x' in value) and ('y' in value) and ('width' in value) and ('height' in value):
                extract.setdefault(frame, {})
                extract[frame].setdefault('{0}_x'.format(key), []).append(value['x'])
                extract[frame].setdefault('{0}_y'.format(key), []).append(value['y'])
                extract[frame].setdefault('{0}_width'.format(key), []).append(value['width'])
                extract[frame].setdefault('{0}_height'.format(key), []).append(value['height'])
    return extract
