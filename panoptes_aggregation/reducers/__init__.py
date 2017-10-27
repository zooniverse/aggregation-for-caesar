from .point_reducer import point_reducer
from .question_reducer import question_reducer
from .survey_reducer import survey_reducer
from .poly_line_text_reducer import poly_line_text_reducer
from .process_kwargs import process_kwargs
from .sw_variant_reducer import sw_variant_reducer

reducers = {
    'point_reducer': point_reducer,
    'question_reducer': question_reducer,
    'survey_reducer': survey_reducer,
    'poly_line_text_reducer': poly_line_text_reducer,
    'sw_variant_reducer': sw_variant_reducer
}
