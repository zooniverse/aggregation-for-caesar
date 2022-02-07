"""
First N False Reducer
--------------------
This module is designed to reduce boolean-valued extracts e.g.
:mod:`panoptes_aggregation.extractors.all_tasks_empty_extractor`.
It returns true if and only if the first N extracts are `False`.
"""
from .reducer_wrapper import reducer_wrapper
import numpy as np

DEFAULTS = {"n": {"default": 0, "type": int}}


def extractResultKey(extract):
    return extract["result"] if "result" in extract else False


@reducer_wrapper(defaults_data=DEFAULTS)
def first_n_false_reducer(data_list, n=0, **kwargs):
    """Reduce a list of boolean values to a single boolean value.

    Parameters
    ----------
    data_list : list
        A list of dicts containing a "result" key which should correspond with a
        boolean value.

    n: int
        The first n results in `data_list` must be `False`.

    Returns
    -------
    reduction : dict
        `reduction["result"]` is `True` if the first n results in `data_list`
        are `False`. Otherwise `False`.
    """
    return {
        "result": n > 0
        and len(data_list) >= n
        and not np.any(list(map(extractResultKey, data_list[:n])))
    }
