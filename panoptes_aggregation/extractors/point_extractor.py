'''
Point Extractor
---------------
This module provides a function to extract drawn points from panoptes annotations.
'''
from collections import OrderedDict
from .extractor_wrapper import extractor_wrapper
from .tool_wrapper import tool_wrapper


@extractor_wrapper
@tool_wrapper
def point_extractor(classification, **kwargs):
    '''Extract annotations from a point drawing tool into lists.
    This extractor does *not* support extraction from multi-frame subjects or
    subtask extraction.  If either of these are needed use
    :mod:`panoptes_aggregation.extractors.point_extractor_by_frame`.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with two keys, `x` and `y`, each containing a list of
        `x` and `y` postions for each marked point

    Examples
    --------
    >>> classification = {'annotations': [
        {
            'task': 'T0',
            'value': [{'tool': 0, 'x': 5, 'y': 10}]
        }
    ]}
    >>> point_extractor(classification)
    {'T0_tool0_x': [5], 'T0_tool0_y': [10]}
    '''
    extract = OrderedDict()
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for idx, value in enumerate(annotation['value']):
            key = '{0}_tool{1}'.format(task_key, value['tool'])
            if ('x' in value) and ('y' in value):
                extract.setdefault('{0}_x'.format(key), []).append(value['x'])
                extract.setdefault('{0}_y'.format(key), []).append(value['y'])
    return extract
