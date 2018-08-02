from functools import wraps
import copy
from panoptes_aggregation import extractors
from slugify import slugify


def subtask_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        details_functions = kwargs.pop('details', None)
        output = func(data, **kwargs)
        human = kwargs.get('human', False)
        if details_functions is not None:
            blank_annotation = {'annotations': {'ST': []}}
            for annotation in data['annotations']:
                if human and ('task_label' in annotation):
                    task_key = slugify(annotation['task_label'], separator='-')
                else:
                    task_key = annotation['task']
                for value in annotation['value']:
                    key_prefix_original = '{0}_tool{1}'.format(annotation['task'], value['tool'])
                    if human and ('tool_label' in value):
                        key_prefix = '{0}_{1}'.format(task_key, slugify(value['tool_label'], separator='-'))
                    else:
                        key_prefix = key_prefix_original
                    key = '{0}_details'.format(key_prefix)
                    frame = 'frame{0}'.format(value['frame'])
                    if key_prefix_original in details_functions:
                        output[frame].setdefault(key, []).append([])
                        for ddx, detail in enumerate(value['details']):
                            mock_annotation = copy.deepcopy(blank_annotation)
                            mock_annotation['annotations']['ST'].append(detail)
                            if details_functions[key_prefix_original][ddx] in extractors.extractors:
                                extractor = extractors.extractors[details_functions[key_prefix_original][ddx]]
                                detail_extract = extractor(mock_annotation)
                                output[frame][key][-1].append(detail_extract)
                            else:
                                output[frame][key][-1].append('No extractor for this subtask type')
        return output
    return wrapper
