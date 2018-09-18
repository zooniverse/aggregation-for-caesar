'''
Rectangle Extractor
-------------------
This module provides a function to extract drawn rectangles from panoptes annotations.
'''
from collections import OrderedDict
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper


@extractor_wrapper
@tool_wrapper
@subtask_wrapper
def rectangle_extractor(classification, **kwargs):
    '''Extact rectangle data from annotation

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains
        the `x`, `y`, `width`, and `height` values for each tool used in
        the annotation.  These are lists that contain one value for each
        rectangle drawn for each tool.
    '''
    extract = OrderedDict()
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for value in annotation['value']:
            key = '{0}_tool{1}'.format(task_key, value['tool'])
            frame = 'frame{0}'.format(value['frame'])
            if ('x' in value) and ('y' in value) and ('width' in value) and ('height' in value):
                extract.setdefault(frame, {})
                extract[frame].setdefault('{0}_x'.format(key), []).append(value['x'])
                extract[frame].setdefault('{0}_y'.format(key), []).append(value['y'])
                extract[frame].setdefault('{0}_width'.format(key), []).append(value['width'])
                extract[frame].setdefault('{0}_height'.format(key), []).append(value['height'])
    return extract
