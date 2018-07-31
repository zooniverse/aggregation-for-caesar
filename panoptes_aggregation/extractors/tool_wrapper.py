from functools import wraps


def tool_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        if 'tools' in kwargs:
            tools = kwargs.pop('tools')
            for annotation in data['annotations']:
                new_value = []
                for v in annotation['value']:
                    if v['tool'] in tools:
                        new_value.append(v)
                annotation['value'] = new_value
        return func(data, **kwargs)
    return wrapper
