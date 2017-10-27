from .point_extractor import point_extractor
from .question_extractor import question_extractor
from .survey_extractor import survey_extractor
from .poly_line_text_extractor import poly_line_text_extractor
from .sw_extractor import sw_extractor
from .sw_variant_extractor import sw_variant_extractor
from .workflow_extractor_config import workflow_extractor_config
from .filter_annotations import filter_annotations

extractors = {
    'point_extractor': point_extractor,
    'question_extractor': question_extractor,
    'survey_extractor': survey_extractor,
    'poly_line_text_extractor': poly_line_text_extractor,
    'sw_extractor': sw_extractor,
    'sw_variant_extractor': sw_variant_extractor
}
