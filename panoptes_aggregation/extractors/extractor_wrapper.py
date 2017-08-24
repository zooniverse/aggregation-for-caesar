from functools import wraps


def unpack_annotations(annotations):
    annotations_list = []
    for value in annotations:
        if isinstance(value, list):
            annotations_list += value
        else:
            annotations_list.append(value)
    return annotations_list


def extractor_wrapper(func):
    @wraps(func)
    def wrapper(argument):
        #: check if argument is a flask request
        if hasattr(argument, 'get_json'):
            data = argument.get_json()
            annotations = data['annotations']
            annotations_list = unpack_annotations(annotations)
            data['annotations'] = annotations_list
            return func(data)
        else:
            return func(argument)
    wrapper._original = func
    return wrapper
