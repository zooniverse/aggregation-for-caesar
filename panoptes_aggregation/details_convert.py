def details_flatten(details):
    """
    Convert the details keyword from classifier 1.0 to 2.0 format.
    The flattened version is what the classifier 2.0 subtask extractor and
    reducer wrappers expect.  As there is no way to tell a 1.0 from a 2.0
    workflow from it's config, this has to be done within the wrappers.
    """
    details_flatten = {}
    for key, value in details.items():
        if type(value) is list:
            names = key.split('_')
            task = names[0]
            toolIndex = names[1][4:]
            for subtaskIndex, item in enumerate(value):
                details_flatten[f'{task}_toolIndex{toolIndex}_subtask{subtaskIndex}'] = item
        elif (type(value) is str) or (value is None):
            # already flat
            details_flatten[key] = value
    return details_flatten


def details_unflatten(details):
    """
    Convert the details keyword from classifier 2.0 to 1.0 format.
    The unflattened version is what the classifier 1.0 subtask extractor and
    reducer wrappers expect.  As there is no way to tell a 1.0 from a 2.0
    workflow from it's config, this has to be done within the wrappers.
    """
    details_unflatten = {}
    holder = {}
    for key, value in details.items():
        if (type(value) is str) or (value is None):
            names = key.split('_')
            task = names[0]
            tool = names[1][9:]
            subtaskIndex = names[2][7:]
            details_key = f'{task}_tool{tool}'
            holder.setdefault(details_key, []).append((subtaskIndex, value))
        elif type(value) is list:
            # already unflat
            details_unflatten[key] = value
    for key, value in holder.items():
        sorted_value = sorted(value, key=lambda x: x[0])
        details_unflatten[key] = [x[1] for x in sorted_value]
    return details_unflatten
