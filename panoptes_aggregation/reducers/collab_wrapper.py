from functools import wraps

def collab_wrapper(func):
    @wraps(func)
    def wrapper(argument, **kwargs):
        collab = kwargs.pop('collab', False)
        step_key = kwargs.pop('step_key', 'S0')
        task_index = kwargs.pop('task_index', 0)
        tool_type = kwargs.pop('tool_type', 'freehandLine')

        # run the original reducer
        clusters = func(argument, **kwargs)

        if collab:
            # classifier v2.0
            if 'toolIndex' in tool:
                tool_split = tool.split("_toolIndex")
                task_key = tool_split[0]
                tool_index = tool_split[1]
            # classifier v1.0
            elif 'tool' in tool:
                tool_split = tool.split("_tool")
                task_key = tool_split[0]
                tool_index = tool_split[1]

            frame_split = frame.split("frame")
            frame_num = frame_split[1]

            x = average_polygon[:, 0].tolist()
            y = average_polygon[:, 1].tolist()

            annotations = {
                'stepKey': step_key,
                'taskIndex': task_index,
                'taskKey': task_key,
                'taskType': 'drawing',
                'toolIndex': int(tool_index),
                'frame': int(frame_num),
                'markID': f'consensus_{counter}',
                'toolType': tool_type,
                'pathX': x,
                'pathY': y
            }

            clusters.setdefault('data', []).append(annotations)
            counter += 1

        return OrderedDict(sorted(clusters.items()))
    return wrapper
