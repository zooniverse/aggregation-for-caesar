from ..shape_tools import SHAPE_LUT
from .shape_normalization import SHAPE_NORMALIZATION

import numpy as np

DEFAULTS_PROCESS = {
    'shape': {'default': None, 'type': str},
    'symmetric': {'default': False, 'type': bool}
}


def process_data(data, shape=None, symmetric=False):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.shape_extractor.shape_extractor`
    shape: str, keyword, required
        A string indicating what shape the extractions contain. This
        should be the name of one of the pre-defined shape tools.
    symmetric: bool, keyword, optional
        If `True` the extracts will be normalized to account for shape
        symmetries. E.g. an ellipse draw with `angle=180` is normalized
        to have `angle=0`.

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`, ...)
        tuples as a vlaue. Each shape parameter shows up in this list.
    '''
    if shape is None:
        raise KeyError('`shape` must be provided as a keyword')
    if shape not in SHAPE_LUT:
        raise KeyError('`shape` must be one of {0}'.format(list(SHAPE_LUT.keys())))
    shape_params = SHAPE_LUT[shape]
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {
        'shape': shape,
        'symmetric': symmetric
    }
    for frame in unique_frames:
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for d in data:
                if frame in d:
                    data_by_tool[frame].setdefault(tool, [])
                    keys = ['{0}_{1}'.format(tool, param) for param in shape_params]
                    if np.all([k in d[frame] for k in keys]):
                        params_list = list(zip(*(d[frame][k] for k in keys)))
                        if symmetric and shape in SHAPE_NORMALIZATION:
                            params_list = [SHAPE_NORMALIZATION[shape](p) for p in params_list]
                        data_by_tool[frame][tool] += params_list
    return data_by_tool
