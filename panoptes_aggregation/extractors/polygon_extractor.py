'''
Polygon/Freehand Tool Extractor
-------------------------------
This module provides a function to extract polygon and freehand drawn
classifications from panoptes annotations.
'''
from collections import OrderedDict
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper


@extractor_wrapper(gold_standard=True)
@tool_wrapper
@subtask_wrapper
def polygon_extractor(classification, gold_standard=False, **kwargs):
    '''Extact polygon/freehand data from annotation

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations. The x and y data of the classifications needs to
        be in one of the following formats: 'pathX': x and 'pathY': y, or
        'points': {'x': x, 'y': y}.

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains lists
        `pathX` and `pathY`. These are lists of lists, where each inner list of
        `pathX` is the x values, and each inner list of `pathY` is the y
        values, for a particular polygon/freehand drawing. The dictionary also
        contains information if the data is gold standard or not.
    '''
    extract = OrderedDict()
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for value in annotation['value']:
            if 'tool' in value:
                # classifier v1.0
                tool_index = value['tool']
                key = '{0}_tool{1}'.format(task_key, tool_index)
            elif 'toolIndex' in value:
                # classifier v2.0
                tool_index = value['toolIndex']
                key = '{0}_toolIndex{1}'.format(task_key, tool_index)
            else:
                raise KeyError('Neither `tool` or `toolIndex` are in the annotation')

            frame = 'frame{0}'.format(value.get('frame', 0))
            extract.setdefault(frame, {})
            # If in the old polygon tool format
            if 'points' in value.keys():
                x = []
                y = []
                points = value["points"]
                for point in points:
                    x.append(point["x"])
                    y.append(point["y"])
            elif 'pathX' in value.keys():  # If data in new format
                x = value["pathX"]
                y = value["pathY"]
            else:
                raise Exception('Unknown data format for polygon data')
            # Only include extracts with data
            if len(x) > 0:
                extract[frame].setdefault('{0}_{1}'.format(key, 'pathX'), []).append(x)
                extract[frame].setdefault('{0}_{1}'.format(key, 'pathY'), []).append(y)
                extract[frame]['gold_standard'] = gold_standard
    return extract
