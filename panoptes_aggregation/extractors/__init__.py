from . import point_extractor

extractors = {
    'point_extractor': point_extractor.extractor_request
}

extractors_base = {
    'point_extractor': point_extractor.classification_to_extract
}
