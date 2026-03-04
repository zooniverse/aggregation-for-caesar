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
            cluster_items = np.array(clusters.get('cluster_items'))
            n_classifications = np.array(clusters.get('n_classifications', 0))
            if n_classifications and cluster_items is not None:
                threshold = int(cluster_items / n_classifications)
                if threshold >= min_threshold:
                    for frame_key, frame_data in list(clusters.items()):
                        if frame_key.startswith('frame'):
                            frame_split = frame_key.split("frame")
                            frame_num = frame_split[1]
                            for key, value in frame_data.items():
                                # shape dependent code goes
                                # new_dict = shape_dep_fn(...)
                                if key.endswith("_clusters_x"):
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
                                    clusters_x = value
                                    clusters_y = frame_data[f"{base}_clusters_y"]

                                    counter = 0

                                    for i in range(len(clusters_x)):
                                        annotations = {
                                            'cluster_items': cluster_items,
                                            'n_classifications': n_classifications,
                                            'threshold': threshold,
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

                                        # annotations.update(new_dict)

                                        clusters.setdefault('data', []).append(annotations)
                                        counter += 1

        return clusters

    return wrapper
