'''
Line Tool for Text Extractor
----------------------------
This module provides a function to extract panoptes annotations
from projects using a line tool to mark lines of text in a
transcribed document and provide the text as a sub-task.
'''
from collections import OrderedDict
import copy
import numpy as np
from packaging import version
from .extractor_wrapper import extractor_wrapper
from .tool_wrapper import tool_wrapper


@extractor_wrapper(gold_standard=True)
@tool_wrapper
def line_text_extractor(classification, gold_standard=False, **kwargs):
    '''Extract annotations from a line tool with a text sub-task

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with one key for each `frame`. The value for each frame
        is a dict with `text`, a list-of-lists of transcribe lines, `points`, a
        dict with the list-of-lists of `x` and `y` postions of each line,
        and `slope`, a list of the slopes (in deg) of each line drawn.
        For `points` and `text` there is one inner list for each annotaiton made
        on the frame.
    '''
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', []),
        ('slope', [])
    ])
    extract = OrderedDict()
    if len(classification['annotations']) > 0:
        classification_metadata = classification.get('metadata', {})
        classifier_version = version.parse(classification_metadata.get('classifier_version', '1.0'))
        if classifier_version >= version.parse('2.0'):
            # pull out the line task
            annotation = [a for a in classification['annotations'] if a['taskType'] == 'transcription'][0]
            # make subtask look up table
            annotation_text = {
                (a['task'], a['markIndex']): a
                for a in classification['annotations']
                if a['taskType'] == 'text'
            }
        else:
            annotation = classification['annotations'][0]
        for vdx, value in enumerate(annotation['value']):
            frame = 'frame{0}'.format(value['frame'])
            extract.setdefault(frame, copy.deepcopy(blank_frame))
            if classifier_version >= version.parse('2.0'):
                text = annotation_text[(value['details'][0]['task'], vdx)]['value']
            else:
                text = value['details'][0]['value']
            x = [value['x1'], value['x2']]
            y = [value['y1'], value['y2']]
            dx = x[-1] - x[0]
            dy = y[-1] - y[0]
            slope = np.rad2deg(np.arctan2(dy, dx))
            extract[frame]['text'].append([text])
            extract[frame]['points']['x'].append(x)
            extract[frame]['points']['y'].append(y)
            extract[frame]['slope'].append(slope)
            extract[frame]['gold_standard'] = gold_standard
    return extract
