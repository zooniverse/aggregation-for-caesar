'''
Shape Extractor
---------------
This module provides a function to extract drawn shapes from panoptes annotations.
'''
from collections import OrderedDict
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper
from ..shape_tools import SHAPE_LUT


@extractor_wrapper
@tool_wrapper
@subtask_wrapper
def shape_extractor(classification, **kwargs):
    '''Extract shape data from annotations

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotation
    shape: str, keyword, required
        A string indicating what shape the annotation contains. This
        should be the name of one of the pre-defined shape tools.

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains
        the shape defining values for each tool used in the annotation.
        These are lists that contain one value for each shape drawn for
        each tool.
    '''
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
