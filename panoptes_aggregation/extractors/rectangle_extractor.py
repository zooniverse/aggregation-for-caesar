'''
Rectangle Extractor
-------------------
This module provides a function to extract drawn rectangles from panoptes annotations.
'''
from collections import OrderedDict
from slugify import slugify
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper


@extractor_wrapper
@tool_wrapper
@subtask_wrapper
def rectangle_extractor(classification, **kwargs):
    '''Extact rectangle dtata from annotation

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
    human = kwargs.get('human', False)
    for annotation in classification['annotations']:
        if human and ('task_label' in annotation):
            #: we should really add a `short_label` on the workflow so this name can be configured
            task_key = slugify(annotation['task_label'], separator='-')
        else:
            task_key = annotation['task']
        for idx, value in enumerate(annotation['value']):
            if (human) and ('tool_label' in value):
                #: we should really add a `short_label` on the workflow so this name can be configured
                key = '{0}_{1}'.format(task_key, slugify(value['tool_label'], separator='-'))
            else:
                key = '{0}_tool{1}'.format(task_key, value['tool'])
            frame = 'frame{0}'.format(value['frame'])
            if ('x' in value) and ('y' in value) and ('width' in value) and ('height' in value):
                extract.setdefault(frame, {})
                extract[frame].setdefault('{0}_x'.format(key), []).append(value['x'])
                extract[frame].setdefault('{0}_y'.format(key), []).append(value['y'])
                extract[frame].setdefault('{0}_width'.format(key), []).append(value['width'])
                extract[frame].setdefault('{0}_height'.format(key), []).append(value['height'])
    return extract
