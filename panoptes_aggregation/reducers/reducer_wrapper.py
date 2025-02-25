import ast
from functools import wraps
from .process_kwargs import process_kwargs
from ..append_version import append_version, remove_version


def reducer_wrapper(
    process_data=None,
    defaults_process=None,
    defaults_data=None,
    user_id=False,
    created_at=False,
    relevant_reduction=False,
    output_kwargs=False
):
    def decorator(func):
        @wraps(func)
        def wrapper(argument, **kwargs):
            kwargs_process = {}
            kwargs_data = {}
            kwargs_details = {}
            kwargs_extra_data = {}
            #: check if argument is a flask request
            if hasattr(argument, 'get_json'):
                kwargs = argument.args.copy().to_dict()
                argument_json = argument.get_json()
                data_in = [d['data'] for d in argument_json]
                remove_version(data_in)
                if 'details' in kwargs:
                    kwargs_details['details'] = ast.literal_eval(kwargs['details'])
                    kwargs_details['data_in'] = data_in
                if user_id:
                    kwargs_extra_data['user_id'] = [d['user_id'] for d in argument_json]
                if created_at:
                    kwargs_extra_data['created_at'] = [d['created_at'] for d in argument_json]
                if relevant_reduction:
                    kwargs_extra_data['relevant_reduction'] = [d['relevant_reduction'] for d in argument_json]
            else:
                data_in = argument
                remove_version(data_in)
                if 'details' in kwargs:
                    kwargs_details['details'] = kwargs['details']
                    kwargs_details['data_in'] = data_in
                if user_id:
                    kwargs_extra_data['user_id'] = kwargs['user_id']
                if created_at:
                    kwargs_extra_data['created_at'] = kwargs['created_at']
                if relevant_reduction:
                    kwargs_extra_data['relevant_reduction'] = kwargs['relevant_reduction']

            if 'count_threshold' in kwargs.keys():
                count_threshold = kwargs['count_threshold']
                if isinstance(count_threshold, str):
                    count_threshold = ast.literal_eval(count_threshold)
                kwargs_details['count_threshold'] = count_threshold
            if 'skill_threshold' in kwargs.keys():
                skill_threshold = kwargs['skill_threshold']
                if isinstance(skill_threshold, str):
                    skill_threshold = ast.literal_eval(skill_threshold)
                kwargs_details['skill_threshold'] = skill_threshold
            if 'mode' in kwargs:
                kwargs_details['mode'] = kwargs['mode'].strip("\'")
            if 'strategy' in kwargs:
                kwargs_details['strategy'] = kwargs['strategy'].strip("\'")
            if 'focus_classes' in kwargs:
                focus_classes = kwargs['focus_classes']
                if isinstance(focus_classes, str):
                    focus_classes = ast.literal_eval(focus_classes)
                kwargs_details['focus_classes'] = focus_classes

            no_version = kwargs.pop('no_version', False)
            if defaults_process is not None:
                kwargs_process = process_kwargs(kwargs, defaults_process)
            if defaults_data is not None:
                kwargs_data = process_kwargs(kwargs, defaults_data)
            if process_data is not None:
                data = process_data(data_in, **kwargs_process)
            else:
                data = data_in
            reduction = func(data, **kwargs_data, **kwargs_details, **kwargs_extra_data)
            if not no_version:
                append_version(reduction)
            if output_kwargs:
                if isinstance(reduction, list):
                    for r in reduction:
                        r['parameters'] = {**kwargs_data, **kwargs_process}
                else:
                    reduction['parameters'] = {**kwargs_data, **kwargs_process}
            return reduction
        #: keep the original function around for testing
        #: and access by other reducers
        wrapper._original = func
        return wrapper
    return decorator
