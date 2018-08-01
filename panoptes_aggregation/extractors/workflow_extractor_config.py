import copy
from collections import defaultdict

type_to_extractor = {
    'single': 'question_extractor',
    'multiple': 'question_extractor',
    'dropdown': 'dropdown_extractor',
    'survey': 'survey_extractor',
    'point': 'point_extractor_by_frame',
    'rectangle': 'rectangle_extractor'
}


def workflow_extractor_config(tasks, keywords={}):
    extractor_config = defaultdict(list)
    if tasks == {'init': {'question': 'init.question', 'type': 'single', 'answers': []}}:
        # this is Shakespeares World, return the correct config
        # the workflow is not stored in Panoptes
        extractor_config = {
            'question_extractor': [
                {'task': 'T0'},
                {'task': 'T3'}
            ],
            'sw_extractor': [{'task': 'T2'}],
            'sw_variant_extractor': [{'task': 'T2'}],
            'sw_graphic_extractor': [{'task': 'T2'}],
        }
        return extractor_config
    if ('T0' in tasks) and ('annotate-' in tasks['T0']['type']):
        # this is annotate, return the correct config
        extractor_config = {
            'question_extractor': [
                {'task': 'T0'},
                {'task': 'T3'}
            ],
            'sw_extractor': [{'task': 'T2'}],
            'sw_graphic_extractor': [{'task': 'T2'}],
        }
        return extractor_config
    for task_key, task in tasks.items():
        task_config = {}
        if task['type'] == 'drawing':
            task_keywords = keywords.get(task_key, {})
            default_config = {
                'task': task_key,
                'tools': [],
                **task_keywords
            }
            for tdx, tool in enumerate(task['tools']):
                if ((tool['type'] == 'polygon') and
                   (len(tool['details']) == 1) and
                   (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    extractor_key = 'poly_line_text_extractor'
                    task_config.setdefault(extractor_key, default_config)
                    task_config[extractor_key]['tools'].append(tdx)
                elif ((tool['type'] == 'line') and
                      (len(tool['details']) == 1) and
                      (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    extractor_key = 'line_text_extractor'
                    task_config.setdefault(extractor_key, default_config)
                    task_config[extractor_key]['tools'].append(tdx)
                else:
                    default_config['details'] = {}
                    if tool['type'] in type_to_extractor:
                        extractor_key = type_to_extractor[tool['type']]
                        task_config.setdefault(extractor_key, copy.deepcopy(default_config))
                        task_config[extractor_key]['tools'].append(tdx)
                        detail_key = '{0}_tool{1}'.format(task_key, tdx)
                        if len(tool['details']) > 0:
                            details_functions = []
                            for detail in tool['details']:
                                if detail['type'] in type_to_extractor:
                                    details_functions.append(type_to_extractor[detail['type']])
                                else:
                                    details_functions.append(None)
                            task_config[extractor_key]['details'][detail_key] = details_functions
            for key, value in task_config.items():
                extractor_config[key].append(value)
        elif task['type'] in type_to_extractor:
            task_keywords = keywords.get(task_key, {})
            extractor_key = type_to_extractor[task['type']]
            extractor_config[extractor_key].append({
                'task': task_key,
                **task_keywords
            })
    return dict(extractor_config)
