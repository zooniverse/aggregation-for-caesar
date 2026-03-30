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
                        if key.endswith('clusters_count'):
                            # classifier v2.0
                            if 'toolIndex' in key:
                                tool_split = key.split("_toolIndex")
                                task_key = tool_split[0]
                                tool_index_split = tool_split[1]
                                tool_index = tool_index_split.split("_clusters_count")[0]
                            # classifier v1.0
                            elif 'tool' in key:
                                tool_split = key.split("_tool")
                                task_key = tool_split[0]
                                tool_index_split = tool_split[1]
                                tool_index = tool_index_split.split("_clusters_count")[0]
                            base = key[:-len("_clusters_count")]
                            shape = frame_data[f"{base}_shape"]
                            clusters_count = frame_data[f"{base}_clusters_count"]
                            n_classifications = frame_data[f"{base}_n_classifications"]

                            if clusters_count and n_classifications:
                                threshold = []
                                for i in range(len(clusters_count)):
                                    threshold_i = clusters_count[i] / n_classifications[i]
                                    threshold.append(threshold_i)

                            for i in reversed(range(len(clusters_count))):
                                if threshold[i] < min_threshold:
                                    clusters_count.pop(i)
                                    threshold.pop(i)

                                    if 'rectangle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]
                                        clusters_height = frame_data[f"{base}_clusters_height"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)
                                        clusters_width.pop(i)
                                        clusters_height.pop(i)

                                    elif 'polygon' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        consensus = frame_data[f"{base}_consensus"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)
                                        consensus.pop(i)

                                    elif 'circle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_r = frame_data[f"{base}_clusters_r"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)
                                        clusters_r.pop(i)

                                    elif 'column' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]

                                        clusters_x.pop(i)
                                        clusters_width.pop(i)

                                    elif 'ellipse' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_rx = frame_data[f"{base}_clusters_rx"]
                                        clusters_ry = frame_data[f"{base}_clusters_ry"]
                                        clusters_angle = frame_data[f"{base}_clusters_angle"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)
                                        clusters_rx.pop(i)
                                        clusters_ry.pop(i)
                                        clusters_angle.pop(i)

                                    elif 'fullWidthLine' in shape:
                                        clusters_y = frame_data[f"{base}_clusters_y"]

                                        clusters_y.pop(i)

                                    elif 'fullHeightLine' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]

                                        clusters_x.pop(i)

                                    elif 'line' in shape:
                                        clusters_x1 = frame_data[f"{base}_clusters_x1"]
                                        clusters_y1 = frame_data[f"{base}_clusters_y1"]
                                        clusters_x2 = frame_data[f"{base}_clusters_x2"]
                                        clusters_y2 = frame_data[f"{base}_clusters_y2"]

                                        clusters_x1.pop(i)
                                        clusters_y1.pop(i)
                                        clusters_x2.pop(i)
                                        clusters_y2.pop(i)

                                    elif 'point' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)

                                    if 'rotateRectangle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]
                                        clusters_height = frame_data[f"{base}_clusters_height"]
                                        clusters_angle = frame_data[f"{base}_clusters_angle"]

                                        clusters_x.pop(i)
                                        clusters_y.pop(i)
                                        clusters_width.pop(i)
                                        clusters_height.pop(i)
                                        clusters_angle.pop(i)

                            for i in range(len(clusters_count)):
                                if threshold[i] >= min_threshold:
                                    annotations = {
                                        'min_threshold': min_threshold,
                                        'threshold': threshold[i],
                                        'stepKey': step_key,
                                        'taskIndex': task_index,
                                        'taskKey': task_key,
                                        'toolIndex': int(tool_index),
                                        'frame': int(frame_num),
                                        'markID': f'consensus_{i}',
                                        'toolType': tool_type
                                    }

                                    if 'rectangle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]
                                        clusters_height = frame_data[f"{base}_clusters_height"]

                                        annotations.update(
                                            {
                                                'taskType': 'rectangle',
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i],
                                                'pathWidth': clusters_width[i],
                                                'pathHeight': clusters_height[i]
                                            }
                                        )

                                    elif 'polygon' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]

                                        annotations.update(
                                            {
                                                'taskType': 'drawing',
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i]
                                            }
                                        )

                                    elif 'circle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_r = frame_data[f"{base}_clusters_r"]

                                        annotations.update(
                                            {
                                                'taskType': 'circle',
                                                'pathR': clusters_r[i],
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i]
                                            }
                                        )

                                    elif 'column' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]

                                        annotations.update(
                                            {
                                                'taskType': 'column',
                                                'pathX': clusters_x[i],
                                                'pathWidth': clusters_width[i]
                                            }
                                        )

                                    elif 'ellipse' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_rx = frame_data[f"{base}_clusters_rx"]
                                        clusters_ry = frame_data[f"{base}_clusters_ry"]
                                        clusters_angle = frame_data[f"{base}_clusters_angle"]

                                        annotations.update(
                                            {
                                                'taskType': 'ellipse',
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i],
                                                'pathRX': clusters_rx[i],
                                                'pathRY': clusters_ry[i],
                                                'angle': clusters_angle[i]
                                            }
                                        )

                                    elif 'fullWidthLine' in shape:
                                        clusters_y = frame_data[f"{base}_clusters_y"]

                                        annotations.update(
                                            {
                                                'taskType': 'fullWidthLine',
                                                'pathY': clusters_y[i],
                                            }
                                        )

                                    elif 'fullHeightLine' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]

                                        annotations.update(
                                            {
                                                'taskType': 'fullHeightLine',
                                                'pathX': clusters_x[i],
                                            }
                                        )

                                    elif 'line' in shape:
                                        clusters_x1 = frame_data[f"{base}_clusters_x1"]
                                        clusters_y1 = frame_data[f"{base}_clusters_y1"]
                                        clusters_x2 = frame_data[f"{base}_clusters_x2"]
                                        clusters_y2 = frame_data[f"{base}_clusters_y2"]

                                        annotations.update(
                                            {
                                                'taskType': 'line',
                                                'pathX1': clusters_x1[i],
                                                'pathY1': clusters_y1[i],
                                                'pathX2': clusters_x2[i],
                                                'pathY2': clusters_y2[i]
                                            }
                                        )

                                    elif 'point' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]

                                        annotations.update(
                                            {
                                                'taskType': 'point',
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i],
                                            }
                                        )

                                    if 'rotateRectangle' in shape:
                                        clusters_x = frame_data[f"{base}_clusters_x"]
                                        clusters_y = frame_data[f"{base}_clusters_y"]
                                        clusters_width = frame_data[f"{base}_clusters_width"]
                                        clusters_height = frame_data[f"{base}_clusters_height"]
                                        clusters_angle = frame_data[f"{base}_clusters_angle"]

                                        annotations.update(
                                            {
                                                'taskType': 'rotateRectangle',
                                                'pathX': clusters_x[i],
                                                'pathY': clusters_y[i],
                                                'pathWidth': clusters_width[i],
                                                'pathHeight': clusters_height[i],
                                                'angle': clusters_angle[i]
                                            }
                                        )

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
