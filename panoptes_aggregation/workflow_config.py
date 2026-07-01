import copy
from collections import defaultdict
from .details_convert import details_flatten, details_unflatten


type_to_extractor = {
    'single': 'question_extractor',
    'multiple': 'question_extractor',
    'shortcut': 'shortcut_extractor',
    'dropdown': 'dropdown_extractor',
    'survey': 'survey_extractor',
    'point': 'shape_extractor',
    'rectangle': 'shape_extractor',
    'circle': 'shape_extractor',
    'column': 'shape_extractor',
    'graph2dRangeX': 'shape_extractor',
    'ellipse': 'shape_extractor',
    'fullWidthLine': 'shape_extractor',
    'fullHeightLine': 'shape_extractor',
    'line': 'shape_extractor',
    'rotateRectangle': 'shape_extractor',
    'temporalRotateRectangle': 'shape_extractor',
    'temporalPoint': 'shape_extractor',
    'triangle': 'shape_extractor',
    'fan': 'shape_extractor',
    'slider': 'slider_extractor',
    'freehandLine': 'polygon_extractor',
    'polygon': 'polygon_extractor',
    'bezier': 'bezier_extractor',
    'text': 'text_extractor',
    'transcription': 'line_text_extractor'
}

standard_reducers = {
    'question_extractor': 'question_reducer',
    'shortcut_extractor': 'shortcut_reducer',
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
    'polygon_extractor': 'polygon_reducer',
    'bezier_extractor': 'polygon_reducer',
    'slider_extractor': 'slider_reducer',
    'text_extractor': 'text_reducer'
}


def workflow_extractor_config(tasks, keywords={}, use_v1_subtask_config=False):
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
                # typical text subtasks are handled normally
                # only use the special extractors if the task type is `transcription`
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
                        if not use_v1_subtask_config:
                            # convert from v1 subtask config to v2 subtask config
                            details_functions = details_flatten({detail_key: details_functions})
                            task_config[extractor_key]['details'] = details_functions
                        else:
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


def workflow_reducer_config(extractor_config, use_v1_subtask_config=False):
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
                # convert incoming subtask config back to v1 for processing with the old code
                details_in = details_unflatten(task['details'])
                for tool in details_in.keys():
                    details[tool] = []
                    for sub_extractor in details_in[tool]:
                        if sub_extractor is None:
                            details[tool].append(None)
                        else:
                            details[tool].append(standard_reducers[sub_extractor])
                if not use_v1_subtask_config:
                    # convert from v1 subtask config to v2 subtask config
                    details = details_flatten(details)
                reducer_config[reducer_key]['details'] = details
            if 'dot_freq' in task:
                reducer_config[reducer_key]['dot_freq'] = task['dot_freq']
            if 'shape' in task:
                reducer_config[reducer_key]['shape'] = task['shape']
        reducer_config_list.append(reducer_config)
    return reducer_config_list
