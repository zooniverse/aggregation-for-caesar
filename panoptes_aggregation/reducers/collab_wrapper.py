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
        counter = 0
        tool = None

        if collab:
            for key in clusters:
                if key.startswith('frame'):
                    frame_split = key.split("frame")
                    frame_num = frame_split[1]
                    break

            frame_dict = clusters[key]

            for k in frame_dict:
                if k.endswith('_consensus'):
                    tool = k.split('_consensus')[0]
                    break

            if tool is None:
                return clusters

            consensus_x = frame_dict[f"{tool}_clusters_x"]
            consensus_y = frame_dict[f"{tool}_clusters_y"]

            x = consensus_x[0]  # list of all x coordinates
            y = consensus_y[0]  # list of all y coordinates

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
            else:
                return clusters

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

        return clusters
    return wrapper
