type_to_extractor = {
    'single': 'question_extractor',
    'multiple': 'question_extractor',
    'dropdown': 'dropdown_extractor',
    'survey': 'survey_extractor',
    'point': 'point_extractor',
    'rectangle': 'rectangle_extractor'
}


def workflow_extractor_config(tasks, keywords={}):
    extractor_config = {}
    if tasks == {'init': {'question': 'init.question', 'type': 'single', 'answers': []}}:
        # this is Shakespeares World, return the correct config
        # the workflow is not stored in Panoptes
        extractor_config['T0'] = 'question_extractor'
        extractor_config['T2'] = ['sw_extractor', 'sw_variant_extractor', 'sw_graphic_extractor']
        extractor_config['T3'] = 'question_extractor'
        return extractor_config
    if ('T0' in tasks) and ('annotate-' in tasks['T0']['type']):
        # this is annotate, return the correct config
        extractor_config['T0'] = 'question_extractor'
        extractor_config['T2'] = ['sw_extractor', 'sw_graphic_extractor']
        extractor_config['T3'] = 'question_extractor'
    for task_key, task in tasks.items():
        if task['type'] == 'drawing':
            tools_config = {}
            for tdx, tool in enumerate(task['tools']):
                if ((tool['type'] == 'polygon') and
                   (len(tool['details']) == 1) and
                   (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    tools_config.setdefault('poly_line_text_extractor', {'tool': []})['tool'].append(tdx)
                elif ((tool['type'] == 'line') and
                      (len(tool['details']) == 1) and
                      (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    tools_config.setdefault('line_text_extractor', {'tool': []})['tool'].append(tdx)
                else:
                    if tool['type'] in type_to_extractor:
                        tool_key = type_to_extractor[tool['type']]
                        tools_config.setdefault(tool_key, {'tool': [], 'details': {}})['tool'].append(tdx)
                        detail_key = '{0}_tool{1}'.format(task_key, tdx)
                        if len(tool['details']) > 0:
                            details_functions = []
                            for detail in tool['details']:
                                if detail['type'] in type_to_extractor:
                                    details_functions.append(type_to_extractor[detail['type']])
                                else:
                                    details_functions.append(None)
                            tools_config[tool_key]['details'][detail_key] = details_functions
            extractor_config[task_key] = tools_config
            if task_key in keywords:
                extractor_config[task_key]['keywords'] = keywords[task_key]
        elif task['type'] in type_to_extractor:
            extractor_config[task_key] = type_to_extractor[task['type']]
    return extractor_config
