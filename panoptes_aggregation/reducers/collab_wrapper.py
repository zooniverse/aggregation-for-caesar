from functools import wraps
import numpy as np


def collab_wrapper(func):
    '''description

        Parameters
        ----------

        kwargs :
            * `collab` : A boolean indicating whether the annotations column is included in the output. Defaults to False.
            * 'step_key' : Identifies the step key. Defaults to 'S0'.
            * 'task_index' : The task index. Defaults to 0.
            * 'tool_type' : The tool used to create the polygons. Defaults to 'freehandLine'.
            * 'min_threshold' : If the threshold value for a cluster is less than min_threshold, it is not added to the dictionary. Defaults to 0.

        Returns
        -------
        Modifies reduction dict

            * `annotations` : Contains the consensus polygons in the original classification format, which is included in the output if `collab` is set to True. For use with the Zooniverse front-end.
            * `data` : Contains the consensus polygons in the original classification format, which is included in the output if `collab` is set to True. For use with the Zooniverse front-end.
            * `threshold` : For each cluster, the threshold is the number of items in the cluster divided by the total number of classifications.

        '''

    @wraps(func)
    def wrapper(argument, **kwargs):
        collab = kwargs.get('collab')
        step_key = kwargs.get('step_key', 'S0')
        task_index = kwargs.get('task_index', 0)
        tool_type = kwargs.get('tool_type', 'freehandLine')
        min_threshold = kwargs.get('min_threshold', 0)

        clusters = func(argument, **kwargs)

        if not collab:
            return clusters

        if collab:
            for frame_key, frame_data in list(clusters.items()):
                if frame_key.startswith('frame'):
                    frame_split = frame_key.split("frame")
                    frame_num = frame_split[1]
                    for key, value in frame_data.items():
                        # shape dependent code goes
                        # new_dict = shape_dep_fn(...)
                        if key.endswith('clusters_x'):
                            # classifier v2.0
                            if 'toolIndex' in key:
                                tool_split = key.split("_toolIndex")
                                task_key = tool_split[0]
                                tool_index_split = tool_split[1]
                                tool_index = tool_index_split.split("_clusters_x")[0]
                            # classifier v1.0
                            elif 'tool' in key:
                                tool_split = key.split("_tool")
                                task_key = tool_split[0]
                                tool_index_split = tool_split[1]
                                tool_index = tool_index_split.split("_clusters_x")[0]
                            base = key[:-len("_clusters_x")]
                            shape = frame_data[f"{base}_shape"]
                            if 'rectangle' in shape:
                                clusters_width = frame_data[f"{base}_clusters_width"]
                                clusters_height = frame_data[f"{base}_clusters_height"]
                                clusters_x = value
                                clusters_y = frame_data[f"{base}_clusters_y"]
                                clusters_count = frame_data[f"{base}_clusters_count"]
                                n_classifications = frame_data[f"{base}_n_classifications"]

                                if clusters_count and n_classifications:
                                    threshold = []
                                    for i in range(len(clusters_count)):
                                        threshold_i = clusters_count[i]/n_classifications[i]
                                        threshold.append(threshold_i)

                                    for i in reversed(range(len(clusters_x))):
                                        if threshold[i] < min_threshold:
                                            clusters_x.pop(i)
                                            clusters_y.pop(i)
                                            clusters_count.pop(i)
                                            threshold.pop(i)
                                            clusters_width.pop(i)
                                            clusters_height.pop(i)

                                    for i in range(len(clusters_x)):
                                        if threshold[i] >= min_threshold:
                                            annotations = {
                                                'min_threshold': min_threshold,
                                                'threshold': threshold[i],
                                                'stepKey': step_key,
                                                'taskIndex': task_index,
                                                'taskKey': task_key,
                                                'taskType': 'rectangle',
                                                'toolIndex': int(tool_index),
                                                'frame': int(frame_num),
                                                'markID': f'consensus_{i}',
                                                'toolType': tool_type,
                                                'rec_x': clusters_x[i],
                                                'rec_y': clusters_y[i],
                                                'rec_width': clusters_width[i],
                                                'rec_height': clusters_height[i]
                                            }

                                            clusters.setdefault('data', []).append(annotations)


                            elif 'polygon' in shape:
                                clusters_x = value
                                clusters_y = frame_data[f"{base}_clusters_y"]
                                clusters_count = frame_data[f"{base}_clusters_count"]
                                n_classifications = frame_data[f"{base}_n_classifications"]
                                consensus = frame_data[f"{base}_consensus"]

                                if clusters_count and n_classifications:
                                    threshold = []
                                    for i in range(len(clusters_count)):
                                        threshold_i = clusters_count[i] / n_classifications[i]
                                        threshold.append(threshold_i)

                                    for i in reversed(range(len(clusters_x))):
                                        if threshold[i] < min_threshold:
                                            clusters_x.pop(i)
                                            clusters_y.pop(i)
                                            clusters_count.pop(i)
                                            consensus.pop(i)
                                            threshold.pop(i)

                                    for i in range(len(clusters_x)):
                                        if threshold[i] >= min_threshold:
                                            annotations = {
                                                'min_threshold': min_threshold,
                                                'threshold': threshold[i],
                                                'stepKey': step_key,
                                                'taskIndex': task_index,
                                                'taskKey': task_key,
                                                'taskType': 'drawing',
                                                'toolIndex': int(tool_index),
                                                'frame': int(frame_num),
                                                'markID': f'consensus_{i}',
                                                'toolType': tool_type,
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i]
                                            }

                                            # annotations.update(new_dict)

                                            clusters.setdefault('data', []).append(annotations)

                            elif 'circle' in shape:
                                clusters_x = value
                                clusters_y = frame_data[f"{base}_clusters_y"]
                                clusters_r = frame_data[f"{base}_clusters_r"]
                                clusters_count = frame_data[f"{base}_clusters_count"]
                                n_classifications = frame_data[f"{base}_n_classifications"]

                                if clusters_count and n_classifications:
                                    threshold = []
                                    for i in range(len(clusters_count)):
                                        threshold_i = clusters_count[i] / n_classifications[i]
                                        threshold.append(threshold_i)

                                    for i in reversed(range(len(clusters_x))):
                                        if threshold[i] < min_threshold:
                                            clusters_x.pop(i)
                                            clusters_y.pop(i)
                                            clusters_r.pop(i)
                                            clusters_count.pop(i)
                                            threshold.pop(i)

                                    for i in range(len(clusters_x)):
                                        if threshold[i] >= min_threshold:
                                            annotations = {
                                                'min_threshold': min_threshold,
                                                'threshold': threshold[i],
                                                'stepKey': step_key,
                                                'taskIndex': task_index,
                                                'taskKey': task_key,
                                                'taskType': 'circle',
                                                'toolIndex': int(tool_index),
                                                'frame': int(frame_num),
                                                'markID': f'consensus_{i}',
                                                'toolType': tool_type,
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i],
                                                'pathR': clusters_r[i]
                                            }

                                            # annotations.update(new_dict)

                                            clusters.setdefault('data', []).append(annotations)

                    if 'data' in clusters:
                        clusters['data'].sort(
                            key=lambda d: (
                                d['frame'],
                                d['toolIndex'],
                                int(d['markID'].split('_')[1])
                            )
                        )

        return clusters

    return wrapper
