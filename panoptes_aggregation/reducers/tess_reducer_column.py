from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper
from ..shape_tools import SHAPE_LUT
from collections import OrderedDict
from scipy.stats import norm
import numpy as np
import peakutils

DEFAULTS = {
    'x_min': {'default': 0, 'type': float},
    'x_max': {'default': 1200, 'type': float},
    'x_step': {'default': 0.1, 'type': float},
    'thres': {'default': 0.05, 'type': float},
    'min_dist': {'default': 2, 'type': float}
}


def process_data(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.shape_extractor.shape_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`, ...)
        tuples as a vlaue. Each shape parameter shows up in this list.
    '''
    shape_params = SHAPE_LUT['column']
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {
        'count_classified': len(data),
    }
    for frame in unique_frames:
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            data_by_tool[frame].setdefault('{0}_count'.format(tool), 0)
            for d in data:
                if frame in d:
                    data_by_tool[frame]['{0}_count'.format(tool)] += 1
                    data_by_tool[frame].setdefault(tool, [])
                    keys = ['{0}_{1}'.format(tool, param) for param in shape_params]
                    if np.all([k in d[frame] for k in keys]):
                        params_list = list(zip(*(d[frame][k] for k in keys)))
                        data_by_tool[frame][tool] += params_list
    return data_by_tool


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS)
@subtask_wrapper
def tess_reducer_column(
    data_by_tool,
    x_min=DEFAULTS['x_min']['default'],
    x_max=DEFAULTS['x_max']['default'],
    x_step=DEFAULTS['x_step']['default'],
    thres=DEFAULTS['thres']['default'],
    min_dist=DEFAULTS['min_dist']['default'],
):
    count_classified = data_by_tool.pop('count_classified')
    x_eval = np.arange(x_min, x_max + x_step, x_step)
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, tool_data in frame_data.items():
            if tool.endswith('_count'):
                clusters[frame]['{0}_ratio'.format(tool)] = tool_data / (count_classified - tool_data)
            else:
                tick_pdf = np.zeros_like(x_eval)
                for column in tool_data:
                    x = column[0] + (0.5 * column[1])  # center the column
                    width = column[1]
                    tick_pdf += norm.pdf(x_eval, loc=x, scale=width/2.355)  # divide the width by two to use the FWHM instead of the standdard deviation
                peak_indexes = peakutils.indexes(tick_pdf, thres=thres, min_dist=min_dist)
                if len(peak_indexes) > 0:
                    clusters[frame]['{0}_peak_x'.format(tool)] = x_eval[peak_indexes].round(5).tolist()
                    clusters[frame]['{0}_peak_pdf'.format(tool)] = tick_pdf[peak_indexes].round(5).tolist()
                    clusters[frame]['{0}_pdf'.format(tool)] = tick_pdf.round(5).tolist()
                    clusters[frame]['{0}_x_eval'.format(tool)] = x_eval.round(5).tolist()
    return clusters
