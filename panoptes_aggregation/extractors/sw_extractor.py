'''
Shakespeares World Text Extractor
---------------------------------
This module provides a fuction to extract the `text` data from
annotations made on Shakespeares World and AnnoTate.
'''
import bs4
from collections import OrderedDict
import copy
import numpy as np
import html
import warnings
from .extractor_wrapper import extractor_wrapper

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

tag_whitelist = [
    'sw-ex',
    'sl',
    'brev-y',
    'sw-ins',
    'sw-del',
    'sw-unclear',
    'sw-sup',
    'label',
    'graphic'
]


def clean_text(s):
    '''
    Clean text from Shakespeares World and AnnoTate classification to prepare
    it for aggregation.  Unicode characters, `xml`, and `html` are removed.

    Parameters
    ----------
    s : string
        A string to be cleaned

    Returns
    -------
    clean_s : string
        The string with all unicode, `xml`, and `html` removed
    '''
    s_out = s.encode('ascii', 'ignore').decode('ascii')
    if '<xml>' in s_out:
        # the user copy and pasted in from micorsoft office
        # these classifications are a mess, just strip all tags
        soup = bs4.BeautifulSoup(s_out, 'lxml')
        s_out = soup.get_text().replace('\n', '')
    elif '<' in s_out:
        # remove html tags (these should never have been in the text to begin with)
        soup = bs4.BeautifulSoup(s_out, 'html.parser')
        for match in soup.findAll():
            if (match.text.strip() == '') or (match.name not in tag_whitelist):
                match.unwrap()
        s_out = str(soup)
    # unescape html and repalce &nbsp; (\xa0) with a normal space
    s_out = html.unescape(s_out).replace('\xa0', ' ')
    return s_out


@extractor_wrapper
def sw_extractor(classification, **kwargs):
    '''Extract text annotations from Shakespeares World and AnnoTate.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        A dictionary with one key for each `frame`. The value for each frame
        is a dict with `text`, a list-of-lists of transcribe words, `points`, a
        dict with the list-of-lists of `x` and `y` postions of each space between words,
        and `slope`, a list of the slopes (in deg) of each line drawn.
        For `points` and `text` there is one inner list for each annotaiton made
        on the frame.
    '''
    extract = OrderedDict()
    blank_frame = OrderedDict([
        ('points', OrderedDict([('x', []), ('y', [])])),
        ('text', []),
        ('slope', [])
    ])
    frame = 'frame0'
    extract[frame] = copy.deepcopy(blank_frame)
    if len(classification['annotations']) > 0:
        annotation = classification['annotations'][0]
        if isinstance(annotation['value'], list):
            for value in annotation['value']:
                if ('startPoint' in value) and ('endPoint' in value) and ('text' in value):
                    x = [value['startPoint']['x'], value['endPoint']['x']]
                    y = [value['startPoint']['y'], value['endPoint']['y']]
                    if (None not in x) and (None not in y):
                        text = [clean_text(value['text'])]
                        dx = x[-1] - x[0]
                        dy = y[-1] - y[0]
                        slope = np.rad2deg(np.arctan2(dy, dx))
                        extract[frame]['text'].append(text)
                        extract[frame]['points']['x'].append(x)
                        extract[frame]['points']['y'].append(y)
                        extract[frame]['slope'].append(slope)
    return extract
