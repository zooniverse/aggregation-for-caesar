'''
Text Tool Reducer
-----------------
This module provides functions to reducer the panoptes text tool into an
alignment table.
'''
import collatex as col
from .text_utils import consensus_score, tokenize
from .reducer_wrapper import reducer_wrapper

# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def process_data(data_list):
    '''Flatten list of extracts into a list of strings.  Empty strings
    are not returned'''
    return [d['text'] for d in data_list if d['text'].strip() != '']


@reducer_wrapper(process_data=process_data)
def text_reducer(data, **kwargs):
    '''Reduce a list of text into an alignment table
    Parameters
    ----------
    data : list
        A list of strigs to be aligned

    Returns
    -------
    reduction : dict
        A dictionary with the following keys:

        *   `aligned_text`: A list of lists containing the aligned text.
            There is one list for each identified word, and each of those lists contains
            one item for each user that entered text. If the user did not transcribe
            a word an empty string is used.
        *   `number_views`: Number of volunteers who entered non-blank text
        *   `consensus_score`: The average number of users who's text agreed.
            Note, if `consensus_score` is the same a `number_views` every user agreed with each other
    '''
    reduction = {}
    if len(data) > 0:
        witness_keys = []
        aligned_text = []
        collation = col.Collation()
        for index, text in enumerate(data):
            key = str(index)
            witness_keys.append(key)
            collation.add_plain_witness(key, text)
        alignment_table = col.collate(collation, near_match=True, segmentation=False)
        for cols in alignment_table.columns:
            word_dict = cols.tokens_per_witness
            word_list = []
            for key in witness_keys:
                word_list.append(str(word_dict.get(key, [''])[0]))
            aligned_text.append(word_list)
        reduction = {
            'aligned_text': aligned_text,
            'number_views': len(data),
            'consensus_score': consensus_score(aligned_text)
        }
    return reduction
