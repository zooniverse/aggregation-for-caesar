from functools import wraps

def collab_wrapper(func):
    @wraps(func)
    def wrapper(argument, **kwargs):
        step_key = kwargs.get('step_key', 'S0')
        task_index = kwargs.get('task_index', 0)
        tool_type = kwargs.get('tool_type', 'freehandLine')

        counter = 0

        clusters = func(argument, **kwargs)

        for frame_key, frame_data in list(clusters.items()):
            if frame_key.startswith('collab'):
                collab = frame_data[0]

        if not collab:
            return clusters

        if collab:
            for frame_key, frame_data in list(clusters.items()):
                if frame_key.startswith('frame'):
                    frame_split = frame_key.split("frame")
                    frame_num = frame_split[1]

                    clusters_x = {}
                    clusters_y = {}

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
                        # shape dependent code goes
                        # new_dict = shape_dep_fn(...)
                        if key.endswith("_clusters_x"):
                            clusters_x = value

                        if key.endswith("_clusters_y"):
                            clusters_y = value

                    for i in range(len(clusters_x)):
                        annotations = {
                            'stepKey': step_key,
                            'taskIndex': task_index,
                            'taskKey': task_key,
                            'taskType': 'drawing',
                            'toolIndex': int(tool_index),
                            'frame': int(frame_num),
                            'markID': f'consensus_{counter}',
                            'toolType': tool_type,
                            'pathX': clusters_x[i],
                            'pathY': clusters_y[i]
                        }
                        #annotations.update(new_dict)

                        clusters.setdefault('data', []).append(annotations)
                        counter += 1

        return clusters

    return wrapper