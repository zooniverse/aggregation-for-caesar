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
    return [
        [idx, str(d.get('text', '')), d.get('gold_standard', False)]
        for idx, d in enumerate(data_list)
        if str(d.get('text', '')).strip() != ''
    ]


@reducer_wrapper(process_data=process_data, user_id=True)
def text_reducer(data_in, **kwargs):
    '''Reduce a list of text into an alignment table
    Parameters
    ----------
    data : list
        A list of strings to be aligned

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
    if len(data_in) > 0:
        user_ids_input = kwargs.pop('user_id')
        idx, data, gold_standard = zip(*data_in)
        user_ids = [user_ids_input[i] for i in idx]
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
        consensus_score_value, consensus_text = consensus_score(aligned_text)
        reduction = {
            'aligned_text': aligned_text,
            'number_views': len(data),
            'consensus_score': consensus_score_value,
            'consensus_text': consensus_text,
            'gold_standard': list(gold_standard),
            'user_ids': user_ids
        }
    return reduction
