'''
Shakespeares World Graphic Extractor
------------------------------------
This module provides a fuction to extract the `graphic` data from
annotations made on Shakespeares World and AnnoTate.
'''
from .extractor_wrapper import extractor_wrapper
from collections import OrderedDict


def exist_and_finite(d, key):
    return (key in d) and (d[key] != 'NaN')


@extractor_wrapper
def sw_graphic_extractor(classification, **kwargs):
    '''Extract all graphics data from a classification

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        Shakespeares World or AnnoTate annotations

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains
        the `x`, `y`, `width`, and `height` values for each tool used in
        the annotation.  These are lists that contain one value for each
        rectangle drawn for each tool.
    '''
    extract = OrderedDict()
    frame = 'frame0'
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        if isinstance(annotation['value'], list):
            for value in annotation['value']:
                if ('type' in value) and ((value['type'] == 'graphic') or (value['type'] == 'image')):
                    exist = exist_and_finite(value, 'x') and exist_and_finite(value, 'y') and exist_and_finite(value, 'width') and exist_and_finite(value, 'height')
                    if (value['type'] == 'graphic'):
                        exist = exist and exist_and_finite(value, 'tag')
                        if exist:
                            extract.setdefault(frame, OrderedDict())
                            extract[frame].setdefault('tool0_tag', []).append(value['tag'])
                    if exist:
                        extract.setdefault(frame, OrderedDict())
                        extract[frame].setdefault('tool0_x', []).append(float(value['x']))
                        extract[frame].setdefault('tool0_y', []).append(float(value['y']))
                        extract[frame].setdefault('tool0_width', []).append(float(value['width']))
                        extract[frame].setdefault('tool0_height', []).append(float(value['height']))
    return extract
