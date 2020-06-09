from functools import wraps
import numpy as np
from collections import defaultdict
from panoptes_aggregation import reducers
from packaging import version


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        details_functions = kwargs.pop('details', None)
        user_id = np.array(kwargs.pop('user_id', []))
        # data_in is the list of original extracts
        # data is the `processed` data_in
        data_in = kwargs.pop('data_in', None)
        output = func(data, **kwargs)
        if details_functions is not None:
            classifier_versions = np.array([version.parse(d.pop('classifier_version', '1.0')) for d in data_in])
            if all(classifier_versions == version.parse('1.0')):
                # classifier version 1.0
                keys_details = ['{0}_details'.format(k) for k in details_functions.keys()]
                keys_labels = ['{0}_cluster_labels'.format(k) for k in details_functions.keys()]
                keys_clusters = ['{0}_clusters_details'.format(k) for k in details_functions.keys()]
                user_ids_per_subtask = defaultdict(lambda: defaultdict(list))
                for edx, extract in enumerate(data_in):
                    for frame_key, frame in extract.items():
                        for k in keys_details:
                            output[frame_key].setdefault(k, [])
                            if k in frame:
                                output[frame_key][k] += frame[k]
                                user_ids_per_subtask[frame_key][k] += [user_id[edx]] * len(frame[k])
                for frame_key, _frame in output.items():
                    for kd, kl, kc, df in zip(keys_details, keys_labels, keys_clusters, details_functions.keys()):
                        detail_array = np.array(output[frame_key][kd])
                        user_id_array = np.array(user_ids_per_subtask[frame_key][kd])
                        if kl in output[frame_key]:
                            cluster_labels = np.array(output[frame_key][kl])
                            for label in np.unique(cluster_labels):
                                if label > -1:
                                    cdx = cluster_labels == label
                                    detail_cluster = detail_array[cdx]
                                    user_id_cluster = user_id_array[cdx]
                                    detail_reduced = []
                                    for ddx, detail in enumerate(detail_cluster.T):
                                        if details_functions[df][ddx] is None:
                                            detail_reduced.append('No reducer for this subtask type')
                                        else:
                                            reducer = reducers.reducers[details_functions[df][ddx]]
                                            detail_reduced.append(
                                                reducer(detail, no_version=True, user_id=user_id_cluster)
                                            )
                                    output[frame_key].setdefault(kc, []).append(detail_reduced)
            elif all(classifier_versions >= version.parse('2.0')):
                # classifier version 2.0 and up
                user_ids_per_subtask = defaultdict(lambda: defaultdict(list))
                for edx, extract in enumerate(data_in):
                    for frame_key, frame in extract.items():
                        for k in details_functions.keys():
                            output[frame_key].setdefault(k, [])
                            if k in frame:
                                output[frame_key][k] += frame[k]
                                user_ids_per_subtask[frame_key][k] += [user_id[edx]] * len(frame[k])
                for frame_key, frame in output.items():
                    unique_tools = set(['_'.join(k.split('_')[:2]) for k in frame.keys()])
                    for tool in unique_tools:
                        subtasks = [k for k in details_functions.keys() if k.startswith(tool)]
                        for subtask in subtasks:
                            cluster_labels = np.array(frame['{0}_cluster_labels'.format(tool)])
                            subtask_array = np.array(frame[subtask])
                            user_id_array = np.array(user_ids_per_subtask[frame_key][subtask])
                            subtask_reduced = []
                            for label in np.unique(cluster_labels):
                                if label > -1:
                                    cdx = cluster_labels == label
                                    subtask_cluster = subtask_array[cdx]
                                    user_id_cluster = user_id_array[cdx]
                                    reducer = reducers.reducers[details_functions[subtask]]
                                    subtask_reduced.append(
                                        reducer(subtask_cluster, no_version=True, user_id=user_id_cluster)
                                    )
                            frame['{0}_clusters'.format(subtask)] = subtask_reduced
                output['classifier_version'] = str(classifier_versions.max())
            else:
                # mix of classifier version 1.0 and 2.0
                # this should never happen
                # chances are this check will need to be done
                # at the reducer wrapper level to prevent the
                # reducer from running in the first place
                pass
        return output
    return wrapper
