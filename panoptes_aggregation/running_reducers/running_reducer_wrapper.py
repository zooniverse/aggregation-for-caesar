import ast
from functools import wraps
from ..reducers.process_kwargs import process_kwargs
from ..append_version import append_version, remove_version


def running_reducer_wrapper(
    process_data=None,
    defaults_process=None,
    defaults_data=None,
    relevant_reduction=False,
    user_id=False
):
    def decorator(func):
        @wraps(func)
        def wrapper(argument, **kwargs):
            kwargs_process = {}
            kwargs_data = {}
            kwargs_extra_data = {}
            #: check if argument is a flask request
            if hasattr(argument, 'get_json'):
                kwargs = argument.args.copy().to_dict()
                argument_json = argument.get_json()
                data_in = [d['data'] for d in argument_json['extracts']]
                store = argument_json['store']
                if 'level_config' in kwargs:
                    kwargs['level_config'] = ast.literal_eval(kwargs['level_config'])
                if user_id:
                    kwargs_extra_data['user_id'] = [d['user_id'] for d in argument_json['extracts']]
                if relevant_reduction:
                    kwargs_extra_data['relevant_reduction'] = [d['relevant_reduction'] for d in argument_json['extracts']]
            else:
                data_in = argument
                store = kwargs['store']
                remove_version(data_in)
                if user_id:
                    kwargs_extra_data['user_id'] = kwargs['user_id']
                if relevant_reduction:
                    kwargs_extra_data['relevant_reduction'] = kwargs['relevant_reduction']
            no_version = kwargs.pop('no_version', False)
            if defaults_process is not None:
                kwargs_process = process_kwargs(kwargs, defaults_process)
            if defaults_data is not None:
                kwargs_data = process_kwargs(kwargs, defaults_data)
            if process_data is not None:
                data = process_data(data_in, **kwargs_process)
            else:
                data = data_in
            reduction = func(data, store=store, **kwargs_data, **kwargs_extra_data)
            if not no_version:
                append_version(reduction)
            return reduction
        #: keep the original function around for testing
        #: and access by other reducers
        wrapper._original = func
        return wrapper
    return decorator
