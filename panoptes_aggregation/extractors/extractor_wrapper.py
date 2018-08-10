import ast
from functools import wraps
import pkg_resources
__version__ = pkg_resources.get_distribution('panoptes_aggregation').version


def append_version(extraction):
    if isinstance(extraction, list):
        for extract in extraction:
            extract['aggregation_version'] = __version__
    else:
        extraction['aggregation_version'] = __version__


def unpack_annotations(annotations, task):
    if task == 'all':
        annotations_list = []
        for value in annotations.values():
            if isinstance(value, list):
                annotations_list += value
            else:
                annotations_list.append(value)
    else:
        annotations_list = annotations.get(task, [])
    return annotations_list


def extractor_wrapper(func):
    @wraps(func)
    def wrapper(argument, **kwargs):
        #: check if argument is a flask request
        if hasattr(argument, 'get_json'):
            kwargs = argument.args.copy().to_dict()
            if 'details' in kwargs:
                kwargs['details'] = ast.literal_eval(kwargs['details'])
            if 'tools' in kwargs:
                kwargs['tools'] = ast.literal_eval(kwargs['tools'])
            data = argument.get_json()
        else:
            data = argument
        task = kwargs.pop('task', 'all')
        no_version = kwargs.pop('no_version', False)
        annotations = data['annotations']
        annotations_list = unpack_annotations(annotations, task)
        data['annotations'] = annotations_list
        extraction = func(data, **kwargs)
        # add package version to the extracted content
        if not no_version:
            append_version(extraction)
        return extraction
    wrapper._original = func
    return wrapper
