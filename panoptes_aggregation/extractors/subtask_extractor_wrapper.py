from functools import wraps
import copy
from panoptes_aggregation import extractors
from panoptes_aggregation.details_convert import details_flatten, details_unflatten
from packaging import version


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        classification_metadata = data.get('metadata', {})
        classifier_version = version.parse(classification_metadata.get('classifier_version', '1.0'))
        details_functions = kwargs.pop('details', None)
        if classifier_version >= version.parse('2.0'):
            # split drawing annotations from subtask annotations
            data_drawing = {'annotations': []}
            data_subtask = {}
            for annotation in data['annotations']:
                # `dataVisAnnotation` is used for graph subjects
                if annotation.get('taskType', 'drawing') in ['drawing', 'dataVisAnnotation']:
                    data_drawing['annotations'].append(annotation)
                else:
                    # if the task is specified this should not be needed
                    # but it is good to be safe
                    if 'markIndex' in annotation:
                        subtask_key = annotation['task']
                        subtask_mark = annotation['markIndex']
                        data_subtask[(subtask_key, subtask_mark)] = annotation
            output = func(data_drawing, **kwargs)
            output['classifier_version'] = str(classifier_version)
        else:
            output = func(data, **kwargs)
        if details_functions is not None:
            if classifier_version < version.parse('2.0'):
                # old classifier version
                # ensure details config matches v1.0 style
                details_functions_v1 = details_unflatten(details_functions)
                blank_annotation = {'annotations': {'ST': []}}
                for annotation in data['annotations']:
                    task_key = annotation['task']
                    for value in annotation['value']:
                        key_prefix = '{0}_tool{1}'.format(task_key, value['tool'])
                        key = '{0}_details'.format(key_prefix)
                        frame = 'frame{0}'.format(value['frame'])
                        if key_prefix in details_functions_v1:
                            output[frame].setdefault(key, []).append([])
                            for ddx, detail in enumerate(value['details']):
                                mock_annotation = copy.deepcopy(blank_annotation)
                                mock_annotation['annotations']['ST'].append(detail)
                                if details_functions_v1[key_prefix][ddx] in extractors.extractors:
                                    extractor = extractors.extractors[details_functions_v1[key_prefix][ddx]]
                                    detail_extract = extractor(mock_annotation, no_version=True)
                                    output[frame][key][-1].append(detail_extract)
                                else:
                                    output[frame][key][-1].append('No extractor for this subtask type')
            else:
                # new classifier version
                # ensure details config matches v2.0 style
                details_functions_v2 = details_flatten(details_functions)
                for annotation in data_drawing['annotations']:
                    task_key = annotation['task']
                    for vdx, value in enumerate(annotation['value']):
                        # if no tools are specified the 'markIndex' key is not set
                        # in this case the annotations have not been filtered so
                        # vdx is the correct value
                        markIndex = value.get('markIndex', vdx)
                        frame = 'frame{0}'.format(value['frame'])
                        for detail in value['details']:
                            subtask = detail['task']
                            subtask_key = '{0}_toolIndex{1}_subtask{2}'.format(*subtask.split('.'))
                            if subtask_key in details_functions_v2:
                                output[frame].setdefault(subtask_key, [])
                                if details_functions_v2[subtask_key] in extractors.extractors:
                                    extractor = extractors.extractors[details_functions_v2[subtask_key]]
                                    try:
                                        subtask_annotation = {'annotations': {
                                            subtask_key: [data_subtask[(subtask, markIndex)]]
                                        }}
                                    except:
                                        print(value)
                                        raise
                                    detail_extract = extractor(subtask_annotation, no_version=True)
                                    output[frame][subtask_key].append(detail_extract)
                                else:
                                    output[frame][subtask_key].append('No extractor for this subtask type')
        return output
    return wrapper
