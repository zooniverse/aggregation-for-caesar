from ..shape_tools import SHAPE_LUT, SHAPE_LUT_FEM
from .shape_normalization import SHAPE_NORMALIZATION, SHAPE_VERSION_CONVERT
from packaging import version

import numpy as np
import re

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
        tuples as a value. Each shape parameter shows up in this list.
    '''
    if shape is None:
        raise KeyError('`shape` must be provided as a keyword')
    if (shape not in SHAPE_LUT) and (shape not in SHAPE_LUT_FEM):
        all_keys = list(set(SHAPE_LUT.keys()).union(set(SHAPE_LUT_FEM.keys())))
        raise KeyError('`shape` must be one of {0}'.format(all_keys))
    unique_frames = set(sum([[k for k in d.keys() if k.startswith('frame')] for d in data], []))
    data_by_tool = {
        'shape': shape,
        'symmetric': symmetric
    }
    classifier_versions = np.array([version.parse(d.get('classifier_version', '1.0')) for d in data])
    mixed = False
    if all(classifier_versions == version.parse('1.0')):
        output_classifier_version = '1.0'
    elif all(classifier_versions >= version.parse('2.0')):
        output_classifier_version = str(classifier_versions.max())
    else:
        mixed = True
        output_classifier_version = str(classifier_versions.max())
    data_by_tool['classifier_version'] = output_classifier_version

    pattern = r'(T[0-9]+)_(tool[Index]*[0-9]+)'

    for frame in unique_frames:
        data_by_tool[frame] = {}
        unique_tools = set(sum([["_".join(re.findall(pattern, k)[0]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            tool_out = tool
            if mixed and ('Index' not in tool):
                # to gracefully handel mixed v1 and v2 need to specify output labels correctly
                tool_out = tool.replace('tool', 'toolIndex')
            for idx, d in enumerate(data):
                classifier_version = classifier_versions[idx]
                if classifier_version == version.parse('1.0'):
                    shape_params = SHAPE_LUT[shape]
                elif classifier_version >= version.parse('2.0'):
                    shape_params = SHAPE_LUT_FEM[shape]
                if frame in d:
                    keys = ['{0}_{1}'.format(tool, param) for param in shape_params]
                    data_by_tool[frame].setdefault(tool_out, [])
                    if np.all([k in d[frame] for k in keys]):
                        params_list = list(zip(*(d[frame][k] for k in keys)))
                        if symmetric and shape in SHAPE_NORMALIZATION:
                            params_list = [SHAPE_NORMALIZATION[shape](p, classifier_version=str(classifier_version)) for p in params_list]
                        if mixed and classifier_version == version.parse('1.0') and shape in SHAPE_VERSION_CONVERT:
                            params_list = [SHAPE_VERSION_CONVERT[shape](p) for p in params_list]
                        data_by_tool[frame][tool_out] += params_list
    return data_by_tool
