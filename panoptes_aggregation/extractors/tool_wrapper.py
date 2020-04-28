from functools import wraps


def tool_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        if 'tools' in kwargs:
            tools = kwargs.pop('tools')
            for annotation in data['annotations']:
                # v1 drawing tasks don't have a `taskType` key
                # default it to `drawing` as there will be only
                # drawing tasks in it
                task_type = annotation.get('taskType', 'drawing')
                if task_type == 'drawing':
                    new_value = []
                    for v in annotation['value']:
                        # v1 classifier
                        if ('tool' in v) and (v['tool'] in tools):
                            new_value.append(v)
                        # v2 classifier
                        if ('toolIndex' in v) and (v['toolIndex'] in tools):
                            new_value.append(v)
                    annotation['value'] = new_value
        return func(data, **kwargs)
    return wrapper
