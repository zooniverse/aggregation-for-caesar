from . import point_extractor
from .workflow_extractor_config import workflow_extractor_config
from .filter_annotations import filter_annotations

extractors = {
    'point_extractor': point_extractor.extractor_request
}

extractors_base = {
    'point_extractor': point_extractor.classification_to_extract
}
