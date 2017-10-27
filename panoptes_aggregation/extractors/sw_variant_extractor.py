from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def sw_variant_extractor(classification):
    extract = {}
    variants = []
    annotation = classification['annotations'][0]
    for value in annotation['value']:
        if 'variants' in value:
            variants += value['variants']
    if len(variants) > 0:
        extract['variants'] = variants
    return extract
