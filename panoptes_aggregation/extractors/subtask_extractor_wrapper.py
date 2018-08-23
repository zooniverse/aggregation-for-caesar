from functools import wraps
import copy
from panoptes_aggregation import extractors


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        details_functions = kwargs.pop('details', None)
        output = func(data, **kwargs)
        if details_functions is not None:
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
        return output
    return wrapper
