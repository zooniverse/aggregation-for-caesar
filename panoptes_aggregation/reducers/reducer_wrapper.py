import ast
from functools import wraps
from .process_kwargs import process_kwargs
from ..append_version import append_version, remove_version


def reducer_wrapper(process_data=None, defaults_process=None, defaults_data=None):
    def decorator(func):
        @wraps(func)
        def wrapper(argument, **kwargs):
            kwargs_process = {}
            kwargs_data = {}
            kwargs_details = {}
            #: check if argument is a flask request
            if hasattr(argument, 'get_json'):
                kwargs = argument.args.copy().to_dict()
                data_in = [d['data'] for d in argument.get_json()]
                remove_version(data_in)
                if 'details' in kwargs:
                    kwargs_details['details'] = ast.literal_eval(kwargs['details'])
                    kwargs_details['data_in'] = data_in
            else:
                data_in = argument
                remove_version(data_in)
                if 'details' in kwargs:
                    kwargs_details['details'] = kwargs['details']
                    kwargs_details['data_in'] = data_in
            no_version = kwargs.pop('no_version', False)
            if defaults_process is not None:
                kwargs_process = process_kwargs(kwargs, defaults_process)
            if defaults_data is not None:
                kwargs_data = process_kwargs(kwargs, defaults_data)
            if process_data is not None:
                data = process_data(data_in, **kwargs_process)
            else:
                data = data_in
            reduction = func(data, **kwargs_data, **kwargs_details)
            if not no_version:
                append_version(reduction)
            return reduction
        #: keep the orignal function around for testing
        #: and access by other reducers
        wrapper._original = func
        return wrapper
    return decorator
