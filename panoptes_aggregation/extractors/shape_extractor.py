'''
Rectangle Extractor
-------------------
This module provides a function to extract drawn shapes from panoptes annotations.
'''
from collections import OrderedDict
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper

SHAPE_LUT = {
    'circle': ['x', 'y', 'r'],
    'column': ['x', 'width'],
    'ellipse': ['x', 'y', 'rx', 'ry', 'angle'],
    'fullWidthLine': ['y'],
    'fullHeightLine': ['x'],
    'line': ['x1', 'y1', 'x2', 'y2'],
    'point': ['x', 'y'],
    'rectangle': ['x', 'y', 'width', 'height'],
    'rotateRectangle': ['x', 'y', 'width', 'height', 'angle'],
    'triangle': ['x', 'y', 'r', 'angle'],
    'fan': ['x', 'y', 'radius', 'rotation', 'spread']
}


@extractor_wrapper
@tool_wrapper
@subtask_wrapper
def shape_extractor(classification, **kwargs):
    '''Extract shape data from annotations'''
    extract = OrderedDict()
    if 'shape' not in kwargs:
        raise KeyError('`shape` must be provided as a keyword')
    shape = kwargs['shape']
    if shape not in SHAPE_LUT:
        raise KeyError('`shape` must be one of {0}'.format(list(SHAPE_LUT.keys())))
    shape_params = SHAPE_LUT[shape]
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for value in annotation['value']:
            key = '{0}_tool{1}'.format(task_key, value['tool'])
            frame = 'frame{0}'.format(value['frame'])
            if all(param in value for param in shape_params):
                extract.setdefault(frame, {})
                for param in shape_params:
                    extract[frame].setdefault('{0}_{1}'.format(key, param), []).append(value[param])
    return extract
