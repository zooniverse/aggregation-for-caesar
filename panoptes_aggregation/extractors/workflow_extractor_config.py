def workflow_extractor_config(tasks):
    extractor_config = {}
    if tasks == {'init': {'question': 'init.question', 'type': 'single', 'answers': []}}:
        # this is Shakespeares World, return the correct config
        # the workflow is not stored in Panoptes
        extractor_config['T0'] = 'question_extractor'
        extractor_config['T2'] = ['sw_extractor', 'sw_variant_extractor', 'sw_graphic_extractor']
        extractor_config['T3'] = 'question_extractor'
        return extractor_config
    for task_key, task in tasks.items():
        if task['type'] == 'drawing':
            tools_config = {}
            for tdx, tool in enumerate(task['tools']):
                if ((tool['type'] == 'polygon') and
                   (len(tool['details']) == 1) and
                   (tool['details'][0]['type'] == 'text')):
                    # this is very ugly but I can't think of a better way to auto detect this
                    tools_config.setdefault('poly_line_text_extractor'.format(tool['type']), []).append(tdx)
                else:
                    tools_config.setdefault('{0}_extractor'.format(tool['type']), []).append(tdx)
            extractor_config[task_key] = tools_config
        elif task['type'] in ['single', 'multiple']:
            extractor_config[task_key] = 'question_extractor'
        elif task['type'] == 'survey':
            extractor_config[task_key] = 'survey_extractor'
    return extractor_config
