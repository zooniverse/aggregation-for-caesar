from functools import wraps

def collab_wrapper(func):
    @wraps(func)
    def wrapper(argument, **kwargs):
        collab = kwargs.get('collab', False)
        step_key = kwargs.get('step_key', 'S0')
        task_index = kwargs.get('task_index', 0)
        tool_type = kwargs.get('tool_type', 'freehandLine')

        counter = 0

        clusters = func(argument, **kwargs)
        clusters_list = list(clusters.items())
        frame_key, frame_data = clusters_list[0]

        if collab:

            frame_split = frame_key.split("frame")
            frame_num = frame_split[1]

            for key, value in frame_data.items():
                if key.endswith("_cluster_labels"):
                    # classifier v2.0
                    if 'toolIndex' in key:
                        tool_split = key.split("_toolIndex")
                        task_key = tool_split[0]
                        tool_index_split = tool_split[1]
                        tool_index = tool_index_split.split("_cluster_labels")[0]
                    # classifier v1.0
                    elif 'tool' in key:
                        tool_split = key.split("_tool")
                        task_key = tool_split[0]
                        tool_index_split = tool_split[1]
                        tool_index = tool_index_split.split("_cluster_labels")[0]

                if key.endswith("_clusters_x"):
                    x = value

                if key.endswith("_clusters_y"):
                    y = value

            annotations = {
                'step_key': step_key,
                'task_index': task_index,
                'task_key': task_key,
                'taskType': 'drawing',
                'tool_index': tool_index,
                'frame': frame_num,
                'markID': f'consensus_{counter}',
                'toolType': tool_type,
                'pathX': x,
                'pathY': y
            }

            clusters.setdefault('data', []).append(annotations)
            counter += 1

        return clusters

    return wrapper