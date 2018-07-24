'''
Point Extractor By Frame
------------------------
This module provides a function to extract drawn points from panoptes annotations.
'''
from collections import OrderedDict
from slugify import slugify
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper


@extractor_wrapper
@subtask_wrapper
def point_extractor_by_frame(classification):
    '''Extract annotations from a point drawing tool into lists

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with one key per frame.  Each frame has two keys, `x` and `y`,
        each containing a list of `x` and `y` postions for each marked point

    Examples
    --------
    >>> classification = {'annotations': [
        {
            'task': 'T0',
            'value': [{'tool': 0, 'x': 5, 'y': 10, 'frame': 0}],
        }
    ]}
    >>> point_extractor(classification)
    {'frame0': {'T0_tool0_x': [5], 'T0_tool0_y': [10]}}
    '''
    extract = OrderedDict()
    for annotation in classification['annotations']:
        if 'task_label' in annotation:
            #: we should really add a `short_label` on the workflow so this name can be configured
            task_key = slugify(annotation['task_label'], separator='-')
        else:
            task_key = annotation['task']
        for idx, value in enumerate(annotation['value']):
            frame = 'frame{0}'.format(value['frame'])
            extract.setdefault(frame, {})
            if 'tool_label' in value:
                #: we should really add a `short_label` on the workflow so this name can be configured
                key = '{0}_{1}'.format(task_key, slugify(value['tool_label'], separator='-'))
            else:
                key = '{0}_tool{1}'.format(task_key, value['tool'])
            if ('x' in value) and ('y' in value):
                extract[frame].setdefault('{0}_x'.format(key), []).append(value['x'])
                extract[frame].setdefault('{0}_y'.format(key), []).append(value['y'])
    return extract
