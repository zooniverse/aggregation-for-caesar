from . import point_extractor
from . import question_extractor
from . import survey_extractor
from .workflow_extractor_config import workflow_extractor_config
from .filter_annotations import filter_annotations

extractors = {
    'point_extractor': point_extractor.point_extractor_request,
    'question_extractor': question_extractor.question_extractor_request,
    'survey_extractor': survey_extractor.survey_extractor_request
}

extractors_base = {
    'point_extractor': point_extractor.classification_to_extract,
    'question_extractor': question_extractor.classification_to_extract,
    'survey_extractor': survey_extractor.classification_to_extract
}
