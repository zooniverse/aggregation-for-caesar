'''
Subject Gold Standard Reducer for difficulty calculation
---------------------------------------------------------
This module provides functions to reduce the gold standard task extracts
to determine a `difficulty' score per subject (defined as the fraction
of succesful classification by all users for that subject)

See also: tess_gold_standard_reducer
'''
from .reducer_wrapper import reducer_wrapper
import numpy as np


@reducer_wrapper()
def subject_difficulty_reducer(extracts):
    '''
    Calculate the difficulty of a gold standard TESS subject

    Parameters
    ----------
    extracts : list
        The list of extracted data including the feedback metadata

    Returns
    -------
    output : dict
        A dictinary with one key `difficulty` that is a list with the fraction of volunteers who
        successfully found each gold standard entry in a subject.
    '''

    feedback_data = [extracti['feedback'] for extracti in extracts if 'feedback' in extracti.keys()]

    output = {}
    if len(feedback_data) > 0:
        success = [feedback['success'] for feedback in feedback_data]
        difficulty = np.mean(success, axis=0)
        output['difficulty'] = difficulty.tolist()
    return output
