from functools import wraps
import copy
from panoptes_aggregation import extractors
from packaging import version


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        classification_metadata = data.get('metadata', {})
        classifier_version = version.parse(classification_metadata.get('classifier_version', '1.0'))
        details_functions = kwargs.pop('details', None)
        if classifier_version >= version.parse('2.0'):
            # split drawing annotaitons from subtask annotations
            data_drawing = {'annotations': []}
            data_subtask = {}
            for annotation in data['annotations']:
                # `dataVisAnnotation` is used for graph subjects
                if annotation.get('taskType', 'drawing') in ['drawing', 'dataVisAnnotation']:
                    data_drawing['annotations'].append(annotation)
                else:
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
                blank_annotation = {'annotations': {'ST': []}}
                for annotation in data['annotations']:
                    task_key = annotation['task']
                    for value in annotation['value']:
                        key_prefix = '{0}_tool{1}'.format(task_key, value['tool'])
                        key = '{0}_details'.format(key_prefix)
                        frame = 'frame{0}'.format(value['frame'])
                        if key_prefix in details_functions:
                            output[frame].setdefault(key, []).append([])
                            for ddx, detail in enumerate(value['details']):
                                mock_annotation = copy.deepcopy(blank_annotation)
                                mock_annotation['annotations']['ST'].append(detail)
                                if details_functions[key_prefix][ddx] in extractors.extractors:
                                    extractor = extractors.extractors[details_functions[key_prefix][ddx]]
                                    detail_extract = extractor(mock_annotation, no_version=True)
                                    output[frame][key][-1].append(detail_extract)
                                else:
                                    output[frame][key][-1].append('No extractor for this subtask type')
            else:
                # new classifier version
                for annotation in data_drawing['annotations']:
                    task_key = annotation['task']
                    for vdx, value in enumerate(annotation['value']):
                        frame = 'frame{0}'.format(value['frame'])
                        for detail in value['details']:
                            subtask = detail['task']
                            subtask_key = '{0}_toolIndex{1}_subtask{2}'.format(*subtask.split('.'))
                            if subtask_key in details_functions:
                                output[frame].setdefault(subtask_key, [])
                                extractor = extractors.extractors[details_functions[subtask_key]]
                                subtask_annotation = {'annotations': {
                                    subtask_key: [data_subtask[(subtask, vdx)]]
                                }}
                                detail_extract = extractor(subtask_annotation, no_version=True)
                                output[frame][subtask_key].append(detail_extract)
        return output
    return wrapper
