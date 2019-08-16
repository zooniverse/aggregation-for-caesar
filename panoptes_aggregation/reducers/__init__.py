from .point_reducer import point_reducer
from .point_reducer_dbscan import point_reducer_dbscan
from .point_reducer_hdbscan import point_reducer_hdbscan
from .rectangle_reducer import rectangle_reducer
from .question_reducer import question_reducer
from .survey_reducer import survey_reducer
from .poly_line_text_reducer import poly_line_text_reducer
from .dropdown_reducer import dropdown_reducer
from .process_kwargs import process_kwargs
from .sw_variant_reducer import sw_variant_reducer
from .shape_reducer_dbscan import shape_reducer_dbscan
from .shape_reducer_hdbscan import shape_reducer_hdbscan
from .slider_reducer import slider_reducer
from .tess_reducer_column import tess_reducer_column
from .tess_gold_standard_reducer import tess_gold_standard_reducer
from .text_reducer import text_reducer
from .optics_line_text_reducer import optics_line_text_reducer
from ..copy_function import copy_function

shortcut_reducer = copy_function(question_reducer, 'shortcut_reducer')

reducers = {
    'point_reducer': point_reducer,
    'point_reducer_dbscan': point_reducer_dbscan,
    'point_reducer_hdbscan': point_reducer_hdbscan,
    'rectangle_reducer': rectangle_reducer,
    'question_reducer': question_reducer,
    'shortcut_reducer': shortcut_reducer,
    'survey_reducer': survey_reducer,
    'poly_line_text_reducer': poly_line_text_reducer,
    'optics_line_text_reducer': optics_line_text_reducer,
    'sw_variant_reducer': sw_variant_reducer,
    'dropdown_reducer': dropdown_reducer,
    'shape_reducer_dbscan': shape_reducer_dbscan,
    'shape_reducer_hdbscan': shape_reducer_hdbscan,
    'slider_reducer': slider_reducer,
    'tess_reducer_column': tess_reducer_column,
    'tess_gold_standard_reducer': tess_gold_standard_reducer,
    'text_reducer': text_reducer
}
