"""
All Tasks Empty Extractor
-------------------------
Extractor determines whether all task values are empty.
"""
from .extractor_wrapper import extractor_wrapper
import numpy as np


@extractor_wrapper()
def all_tasks_empty_extractor(classification, **kwargs):
    """Determine whether all task values in a classification are empty.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations

    Returns
    -------
    extraction : dict
        `extraction["result"]` is `True` if all task values are `None`. `False`
        otherwise.
    """
    empty_or_absent_value = [
        task["value"] is None if "value" in task else True
        for task in classification["annotations"]
    ]

    return {"result": len(empty_or_absent_value) == 0 or np.all(empty_or_absent_value)}
