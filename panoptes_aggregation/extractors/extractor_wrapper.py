import ast
import copy
from functools import wraps
from ..append_version import append_version
from .utilities import pluck_fields


def unpack_annotations(annotations, task):
    annotations_list = []
    for key, value in annotations.items():
        # subtasks are stored as 'T0.0.0' and need to be pulled out with 'T0'
        if (task == 'all') or (key.split('.')[0] == task):
            annotations_list += value
    return annotations_list


def extractor_wrapper(gold_standard=False):
    def decorator(func):
        @wraps(func)
        def wrapper(argument, **kwargs):
            #: check if argument is a flask request

            # create a default value so that
            # we can process entries without the `pluck` parameter
            pluck_key_dict = None

            if hasattr(argument, 'get_json'):
                kwargs = argument.args.copy().to_dict()
                if 'details' in kwargs:
                    kwargs['details'] = ast.literal_eval(kwargs['details'])
                if 'tools' in kwargs:
                    kwargs['tools'] = ast.literal_eval(kwargs['tools'])
                if 'pluck' in kwargs:
                    pluck_key_dict = ast.literal_eval(kwargs['pluck'])

                data = argument.get_json()
            else:
                data = argument
                pluck_key_dict = kwargs.pop('pluck', None)

            # the task key to extract
            task = kwargs.pop('task', 'all')
            # if the task is recursive (i.e. there will be more than one instance of the task per classification)
            recursive = kwargs.pop('recursive', False)
            no_version = kwargs.pop('no_version', False)
            annotations = data['annotations']
            annotations_list = unpack_annotations(annotations, task)
            if gold_standard:
                kwargs['gold_standard'] = data.get('gold_standard', False)
            if recursive:
                # run each annotation through the code as if it was submitted on its own
                # return the list of resulting extracts
                # the extract code will write each item in a new row
                extraction = []
                for annotation in annotations_list:
                    data_recursive = copy.deepcopy(data)
                    data_recursive['annotations'] = [annotation]
                    extraction.append(func(data_recursive, **kwargs))
            else:
                data['annotations'] = annotations_list
                extraction = func(data, **kwargs)

            ''' RS 2021/09/14
            if the pluck parameter exists
            append the required data from the pluckfield extractor
            to the output data
            '''
            if pluck_key_dict is not None:
                # get the data and corresponding keys
                pluck_values = pluck_fields(data, pluck_key_dict)

                # append the data with its corresponding
                # key to the output data
                for key in pluck_values.keys():
                    extraction[key] = pluck_values[key]

            # add package version to the extracted content
            if not no_version:
                append_version(extraction)

            return extraction
        wrapper._original = func
        return wrapper
    return decorator
