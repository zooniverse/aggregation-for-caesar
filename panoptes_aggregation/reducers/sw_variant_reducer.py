from .reducer_wrapper import reducer_wrapper


@reducer_wrapper()
def sw_variant_reducer(extracts):
    reduction = {}
    variants = []
    for e in extracts:
        if 'variants' in e:
            variants += e['variants']
    if len(variants) > 0:
        reduction['variants'] = variants
    return reduction
