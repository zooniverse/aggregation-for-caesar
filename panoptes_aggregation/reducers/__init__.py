from . import cluster_points
from . import question_reducer
from . import survey_reducer
from . import poly_line_text_reducer
from .process_kwargs import process_kwargs

reducers = {
    'point_reducer': cluster_points.point_reducer_request,
    'question_reducer': question_reducer.question_reducer_request,
    'survey_reducer': survey_reducer.survey_reducer_request,
    'poly_line_text_reducer': poly_line_text_reducer.poly_line_text_reducer_request
}

reducer_base = {
    'point_reducer': cluster_points.reducer_base,
    'question_reducer': question_reducer.reducer_base,
    'survey_reducer': survey_reducer.reducer_base,
    'poly_line_text_reducer': poly_line_text_reducer.reducer_base
}
