from .shape_process_data import process_data, DEFAULTS_PROCESS
from .reducer_wrapper import reducer_wrapper
from .subtask_reducer_wrapper import subtask_wrapper
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


@reducer_wrapper(process_data=process_data, defaults_data=DEFAULTS, defaults_process=DEFAULTS_PROCESS)
@subtask_wrapper
def tess_reducer_column(
    data_by_tool,
    x_min=DEFAULTS['x_min']['default'],
    x_max=DEFAULTS['x_max']['default'],
    x_step=DEFAULTS['x_step']['default'],
    thres=DEFAULTS['thres']['default'],
    min_dist=DEFAULTS['min_dist']['default'],
):
    data_by_tool.pop('shape')
    data_by_tool.pop('symmetric')
    x_eval = np.arange(x_min, x_max + x_step, x_step)
    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, tool_data in frame_data.items():
            tick_pdf = np.zeros_like(x_eval)
            for column in tool_data:
                x = column[0] + (0.5 * column[1])  # center the column
                width = column[1]
                tick_pdf += norm.pdf(x_eval, loc=x, scale=width/2.355)  # divide the width by two to use the FWHM instead of the standdard deviation
            peak_indexes = peakutils.indexes(tick_pdf, thres=thres, min_dist=min_dist)
            if len(peak_indexes) > 0:
                clusters[frame]['{0}_peak_x'.format(tool)] = x_eval[peak_indexes].round(5).tolist()
                clusters[frame]['{0}_peak_pdf'.format(tool)] = tick_pdf[peak_indexes].round(5).tolist()
    return clusters
