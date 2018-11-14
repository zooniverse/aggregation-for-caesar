import io
import os
import yaml
import json
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from panoptes_aggregation.workflow_config import workflow_extractor_config, workflow_reducer_config
import pandas


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')
    return file


def config_workflow(
            workflow_csv,
            workflow_id,
            version=None,
            keywords={},
            workflow_content=None,
            minor_version=None,
            language='en',
            output_dir=None
        ):
    workflow_csv = get_file_instance(workflow_csv)
    with workflow_csv as workflow_csv_in:
        workflows = pandas.read_csv(workflow_csv_in, encoding='utf-8')

    if version is None:
        version = workflows[workflows.workflow_id == workflow_id].version.max()
        warnings.warn('No major workflow version was specified, defaulting to version {0}'.format(version))

    wdx = (workflows.workflow_id == workflow_id) & (workflows.version == version)
    assert (wdx.sum() > 0), 'workflow ID and workflow major version combination does not exist'
    assert (wdx.sum() == 1), 'workflow ID and workflow major version combination is not unique'
    workflow = workflows[wdx].iloc[0]
    workflow_tasks = json.loads(workflow.tasks)
    extractor_config = workflow_extractor_config(workflow_tasks, keywords=keywords)
    workflow_version = '{0}'.format(version)
    if minor_version is not None:
        workflow_version = '{0}.{1}'.format(version, minor_version)
    config = {
        'workflow_id': workflow_id,
        'workflow_version': workflow_version,
        'extractor_config': extractor_config
    }
    filename = 'Extractor_config_workflow_{0}_V{1}.yaml'.format(workflow_id, version)
    if output_dir is not None:
        filename = os.path.join(output_dir, filename)
    with open(filename, 'w', encoding='utf-8') as stream:
        yaml.dump(config, stream=stream, default_flow_style=False, indent=4)
        print('Saving Extractor config to:\n{0}'.format(filename))
        print()
    reducer_config_list = workflow_reducer_config(extractor_config)
    task_set = set({})
    for extractor, reducer in zip(sorted(extractor_config.keys()), reducer_config_list):
        reducer_config = {
            'reducer_config': reducer
        }
        filename = 'Reducer_config_workflow_{0}_V{1}_{2}.yaml'.format(workflow_id, version, extractor)
        if output_dir is not None:
            filename = os.path.join(output_dir, filename)
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(reducer_config, stream=stream, default_flow_style=False, indent=4)
            print('Saving Reducer config to:\n{0}'.format(filename))
            print()
        for task in extractor_config[extractor]:
            task_set.add(task['task'])
    if workflow_content is not None:
        workflow_content = get_file_instance(workflow_content)
        with workflow_content as workflow_content_in:
            contents = pandas.read_csv(workflow_content_in, encoding='utf-8')
        if minor_version is None:
            minor_version = contents[contents.workflow_id == workflow_id].version.max()
            warnings.warn('No minor workflow version was specified, defaulting to version {0}'.format(minor_version))
        cdx = (contents.workflow_id == workflow_id) & (contents.version == minor_version)
        if cdx.sum() == 0:
            raise IndexError('workflow ID and workflow minor version combination does not exist')
        if cdx.sum() > 1:
            raise IndexError('workflow ID and workflow mainor version combination is not unique')
        content = contents[cdx].iloc[0]
        strings = eval(content.strings)
        stirngs_extract = {key: value for key, value in strings.items() for task in task_set if (key.startswith(task) and ('help' not in key))}
        filename = 'Task_labels_workflow_{0}_V{1}.{2}.yaml'.format(workflow_id, version, minor_version)
        if output_dir is not None:
            filename = os.path.join(output_dir, filename)
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(stirngs_extract, stream=stream, default_flow_style=False, indent=4)
            print('Saving task key look up table to:\n{0}'.format(filename))
    return config
