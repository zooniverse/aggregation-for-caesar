from collections import OrderedDict
from slugify import slugify
from .extractor_wrapper import extractor_wrapper


@extractor_wrapper
def point_extractor(classification):
    extract = OrderedDict()
    for annotation in classification['annotations']:
        if 'task_label' in annotation:
            # we should really add a `short_label` on the workflow so this name can be configured
            task_key = slugify(annotation['task_label'], separator='-')
        else:
            task_key = annotation['task']
        for idx, value in enumerate(annotation['value']):
            if 'tool_label' in value:
                # we should really add a `short_label` on the workflow so this name can be configured
                key = '{0}_{1}'.format(task_key, slugify(value['tool_label'], separator='-'))
            else:
                key = '{0}_tool{1}'.format(task_key, value['tool'])
            if ('x' in value) and ('y' in value):
                extract.setdefault('{0}_x'.format(key), []).append(value['x'])
                extract.setdefault('{0}_y'.format(key), []).append(value['y'])
    return extract
