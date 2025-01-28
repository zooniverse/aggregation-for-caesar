'''
Polygon/Freehand Tool Extractor
-------------------------------
This module provides a function to extract polygon andfreehand drawn lines
from panoptes annotations.
'''
from collections import OrderedDict
import copy
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
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains
        the `x`, `y`, values for the tool used in
        the polygon.  These are lists that each contain list of the x and
        y values for each drawn polygon. The UTC time when the annotation was
        made and the if the data is gold standard is also extracted.
    '''
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])]))
    ])
    extract = OrderedDict()
    for idx, annotation in enumerate(classification['annotations']):
        time = classification['metadata']['finished_at']
        for vdx, value in enumerate(annotation['value']):
            frame = 'frame{0}'.format(value['frame'])
            extract.setdefault(frame, copy.deepcopy(blank_frame))
            points = value["points"]
            x = []
            y = []
            for point in points:
                x.append(point["x"])
                y.append(point["y"])
            extract[frame]['points']['x'].append(x)
            extract[frame]['points']['y'].append(y)
            extract[frame]['time'] = time
            extract[frame]['gold_standard'] = gold_standard
    return extract
