def filter_annotations(annotations, config, human=False):
    # this is specific to drawing tasks at the moment
    # each tool can use a different extractor
    # this will split the annotations by extractor type
    annotations_by_extractor = {}
    for annotation in annotations:
        if annotation['task'] in config:
            if isinstance(config[annotation['task']], dict):
                for extractor_name, tool_idx in config[annotation['task']].items():
                    annotations_by_extractor.setdefault(extractor_name, [])
                    annotations_by_extractor[extractor_name].append({
                        'task': annotation['task'],
                        'value': []
                    })
                    if human:
                        annotations_by_extractor[extractor_name][-1]['task_label'] = annotation['task_label']
                    for value in annotation['value']:
                        if value['tool'] in tool_idx:
                            if not human:
                                value.pop('tool_label')
                            annotations_by_extractor[extractor_name][-1]['value'].append(value)
            else:
                extractor_name = config[annotation['task']]
                annotations_by_extractor.setdefault(extractor_name, [])
                annotations_by_extractor[extractor_name].append({
                    'task': annotation['task'],
                    'value': annotation['value']
                })
                if human:
                    annotations_by_extractor[extractor_name][-1]['task_label'] = annotation['task_label']
    return annotations_by_extractor
