def workflow_extractor_config(tasks):
    extractor_config = {}
    for task_key, task in tasks.items():
        # only extracts drawing at the moment
        # this config maps the tool number to the extractor type
        if task['type'] == 'drawing':
            tools_config = {}
            for tdx, tool in enumerate(task['tools']):
                tools_config.setdefault('{0}_extractor'.format(tool['type']), []).append(tdx)
            extractor_config[task_key] = tools_config
        elif task['type'] in ['single', 'multiple']:
            extractor_config[task_key] = 'question_extractor'
        elif task['type'] == 'survey':
            extractor_config[task_key] = 'survey_extractor'
    return extractor_config
