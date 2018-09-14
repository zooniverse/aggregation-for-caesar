from functools import wraps
import numpy as np
from panoptes_aggregation import reducers


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        details_functions = kwargs.pop('details', None)
        data_in = kwargs.pop('data_in', None)
        output = func(data, **kwargs)
        if details_functions is not None:
            keys_details = ['{0}_details'.format(k) for k in details_functions.keys()]
            keys_labels = ['{0}_cluster_labels'.format(k) for k in details_functions.keys()]
            keys_clusters = ['{0}_clusters_details'.format(k) for k in details_functions.keys()]
            for extract in data_in:
                for frame_key, frame in extract.items():
                    for k in keys_details:
                        output[frame_key].setdefault(k, [])
                        if k in frame:
                            output[frame_key][k] += frame[k]
            for frame_key, frame in output.items():
                for kd, kl, kc, df in zip(keys_details, keys_labels, keys_clusters, details_functions.keys()):
                    detail_array = np.array(output[frame_key][kd])
                    if kl in output[frame_key]:
                        cluster_labels = np.array(output[frame_key][kl])
                        for label in np.unique(cluster_labels):
                            if label > -1:
                                detail_cluster = detail_array[cluster_labels == label]
                                detail_reduced = []
                                for ddx, detail in enumerate(detail_cluster.T):
                                    if details_functions[df][ddx] is None:
                                        detail_reduced.append('No reducer for this subtask type')
                                    else:
                                        reducer = reducers.reducers[details_functions[df][ddx]]
                                        detail_reduced.append(reducer(detail, no_version=True))
                                output[frame_key].setdefault(kc, []).append(detail_reduced)
        return output
    return wrapper
