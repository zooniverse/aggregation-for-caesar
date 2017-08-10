'''
Polygon As Line Tool for Text Extractor
---------------------------------------
This module provides a fuction of eaxtract panoptes annotations
from porjects using a polygon tool to mark word in a transcribed
document and provide the transcribed text as a sub-task.
'''
from collections import OrderedDict
import copy
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def poly_line_text_extractor(classification):
    '''Extract annotations from a polygon tool with a text sub-task

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with one key for each `frame`. The value for each frame
        is a dict with `text`,a list of transcribe words, and `points`, a
        dict with the list of `x` and `y` postions of each word.

    Examples
    --------
    >>> classification = {'annotations': [
        'value': [
            {
                'frame': 0,
                'points': [
                    {'x': 756, 'y': 197}
                ],
                'details': [
                    {'value': '[unclear]Cipher[/unclear]'}
                ],
            }
    ]}
    >>> poly_line_text_extractor(classification)
    {'frame0': {
        'points': {'x': [756], 'y': [197]},
        'text': ['[unclear]Cipher[/unclear]']
    }}
    '''
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', [])
    ])
    extract = OrderedDict()
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        frame = 'frame{0}'.format(value['frame'])
        extract.setdefault(frame, copy.deepcopy(blank_frame))
        text = value['details'][0]['value']
        words = text.split(' ')
        # NOTE: if `words` and `points` are differnt lengths
        # the extract will only contain the *shorter* of the
        # two lists (assuming they match from the front)
        for word, point in zip(words, value['points']):
            extract[frame]['text'].append(word)
            extract[frame]['points']['x'].append(point['x'])
            extract[frame]['points']['y'].append(point['y'])
    return extract
