import copy
from collections import defaultdict

type_to_extractor = {
    'single': 'question_extractor',
    'multiple': 'question_extractor',
    'shortcut': 'question_extractor',
    'dropdown': 'dropdown_extractor',
    'survey': 'survey_extractor',
    'point': 'point_extractor_by_frame',
    'rectangle': 'shape_extractor',
    'circle': 'shape_extractor',
    'column': 'shape_extractor',
    'ellipse': 'shape_extractor',
    'fullWidthLine': 'shape_extractor',
    'fullHeightLine': 'shape_extractor',
    'line': 'shape_extractor',
    'rotateRectangle': 'shape_extractor',
    'triangle': 'shape_extractor',
    'fan': 'shape_extractor',
    'slider': 'slider_extractor'
}

standard_reducers = {
    'question_extractor': 'question_reducer',
    'dropdown_extractor': 'dropdown_reducer',
    'survey_extractor': 'survey_reducer',
    'point_extractor': 'point_reducer',
    'point_extractor_by_frame': 'point_reducer_dbscan',
    'rectangle_extractor': 'rectangle_reducer',
    'sw_graphic_extractor': 'rectangle_reducer',
    'line_text_extractor': 'poly_line_text_reducer',
    'poly_line_text_extractor': 'poly_line_text_reducer',
    'sw_extractor': 'poly_line_text_reducer',
    'sw_variant_extractor': 'sw_variant_reducer',
    'shape_extractor': 'shape_reducer_dbscan',
    'slider_extractor': 'slider_reducer'
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
                    del task_config[extractor_key]['tools']
                elif ((tool['type'] == 'line') and
                      (len(tool['details']) == 1) and
                      (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    extractor_key = 'line_text_extractor'
                    task_config.setdefault(extractor_key, default_config)
                    del task_config[extractor_key]['tools']
                else:
                    default_config['details'] = {}
                    if tool['type'] in type_to_extractor:
                        extractor_key = type_to_extractor[tool['type']]
                        shape = None
                        if extractor_key == 'shape_extractor':
                            extractor_key = '{0}_{1}'.format(extractor_key, tool['type'])
                            shape = tool['type']
                        task_config.setdefault(extractor_key, copy.deepcopy(default_config))
                        task_config[extractor_key]['tools'].append(tdx)
                        if shape is not None:
                            task_config[extractor_key]['shape'] = shape
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


def workflow_reducer_config(extractor_config):
    reducer_config_list = []
    for extractor in sorted(extractor_config.keys()):
        if 'shape_extractor' in extractor:
            reducer_key = standard_reducers['shape_extractor']
        else:
            reducer_key = standard_reducers[extractor]
        reducer_config = {reducer_key: {}}
        if extractor == 'sw_extractor':
            reducer_config[reducer_key]['dot_freq'] = 'line'
        for task in extractor_config[extractor]:
            if ('details' in task) and (len(task['details']) > 0):
                details = {}
                for tool in task['details'].keys():
                    details[tool] = []
                    for sub_extractor in task['details'][tool]:
                        if sub_extractor is None:
                            details[tool].append(None)
                        else:
                            details[tool].append(standard_reducers[sub_extractor])
                reducer_config[reducer_key]['details'] = details
            if 'dot_freq' in task:
                reducer_config[reducer_key]['dot_freq'] = task['dot_freq']
            if 'shape' in task:
                reducer_config[reducer_key]['shape'] = task['shape']
        reducer_config_list.append(reducer_config)
    return reducer_config_list
