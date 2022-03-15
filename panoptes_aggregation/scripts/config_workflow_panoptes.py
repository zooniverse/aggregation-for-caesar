import io
import os
import yaml
import json
import warnings
import packaging.version
import numpy as np

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from panoptes_aggregation.workflow_config import workflow_extractor_config, workflow_reducer_config
import pandas


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')  # pragma: no cover
    return file


def config_workflow(
    workflow_csv,
    workflow_id,
    version=None,
    min_version=None,
    max_version=None,
    keywords={},
    output_dir=None,
    verbose=False
):
    workflow_csv = get_file_instance(workflow_csv)
    with workflow_csv as workflow_csv_in:
        workflows = pandas.read_csv(workflow_csv_in, encoding='utf-8')

    workflows['version_parse'] = np.array([
        packaging.version.parse('{0}.{1}'.format(v, m))
        for v, m in zip(workflows.version, workflows.minor_version)
    ])

    wdx = (workflows.workflow_id == workflow_id)
    if (version is None) and (min_version is None) and (max_version is None):
        # no version specified, take the latest version of the workflow
        version = workflows[wdx].version_parse.max()
        workflow_version = str(version)
        if verbose:
            warnings.warn('No workflow version was specified, defaulting to version {0}'.format(version))
        wdx &= (workflows.version_parse == version)
    elif (version is None):
        # either min or max version is given
        workflow_version = {}
        if min_version is not None:
            workflow_version['min'] = min_version
            min_version = packaging.version.parse(min_version)
            wdx &= (workflows.version_parse >= min_version)
        if max_version is not None:
            workflow_version['max'] = max_version
            max_version = packaging.version.parse(max_version)
            wdx &= (workflows.version_parse <= max_version)
    else:
        # version is given
        workflow_version = version
        version = packaging.version.parse(version)
        wdx &= (workflows.version_parse == version)

    assert (wdx.sum() > 0), 'workflow ID and workflow version(s) combination does not exist'
    # configure off of the latest workflow when given a range
    configure_version = workflows[wdx].version_parse.max()
    configure_version_loc = workflows[wdx].version_parse.argmax()
    if wdx.sum() > 1:
        warnings.warn('A workflow range was specified, configuration is based on {0}'.format(configure_version))
    workflow = workflows[wdx].iloc[configure_version_loc]
    workflow_tasks = json.loads(workflow.tasks)
    extractor_config = workflow_extractor_config(workflow_tasks, keywords=keywords)
    config = {
        'workflow_id': workflow_id,
        'workflow_version': workflow_version,
        'extractor_config': extractor_config
    }
    # configure the extractors
    filename = 'Extractor_config_workflow_{0}_V{1}.yaml'.format(workflow_id, configure_version)
    if output_dir is not None:
        filename = os.path.join(output_dir, filename)
    with open(filename, 'w', encoding='utf-8') as stream:
        yaml.dump(config, stream=stream, default_flow_style=False, indent=4)
        print('Saving Extractor config to:\n{0}'.format(filename))
        print()
    # configure the reducers
    reducer_config_list = workflow_reducer_config(extractor_config)
    task_set = set({})
    for extractor, reducer in zip(sorted(extractor_config.keys()), reducer_config_list):
        reducer_config = {
            'reducer_config': reducer
        }
        filename = 'Reducer_config_workflow_{0}_V{1}_{2}.yaml'.format(workflow_id, configure_version, extractor)
        if output_dir is not None:
            filename = os.path.join(output_dir, filename)
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(reducer_config, stream=stream, default_flow_style=False, indent=4)
            print('Saving Reducer config to:\n{0}'.format(filename))
            print()
        for task in extractor_config[extractor]:
            task_set.add(task['task'])
    # make the task string look up table
    strings = eval(workflow.strings)
    strings_extract = {key: value for key, value in strings.items() for task in task_set if (key.startswith(task) and ('help' not in key))}
    if 'dropdown_extractor' in extractor_config:
        for dropdown_task in extractor_config['dropdown_extractor']:
            dropdown_task_id = dropdown_task['task']
            dropdown_string_keys = [key for key in strings_extract.keys() if key.startswith(f'{dropdown_task_id}.selects')]
            for dropdown_string_key in dropdown_string_keys:
                task_id, selects, selects_idx, options, star, star_idx, _ = dropdown_string_key.split('.')
                dropdown_label_hash = workflow_tasks[task_id][selects][int(selects_idx)][options][star][int(star_idx)]['value']
                dropdown_label = strings_extract[dropdown_string_key]
                strings_extract[dropdown_string_key] = {dropdown_label_hash: dropdown_label}
    filename = 'Task_labels_workflow_{0}_V{1}.yaml'.format(workflow_id, configure_version)
    if output_dir is not None:
        filename = os.path.join(output_dir, filename)
    with open(filename, 'w', encoding='utf-8') as stream:
        yaml.dump(strings_extract, stream=stream, default_flow_style=False, indent=4)
        print('Saving task key look up table to:\n{0}'.format(filename))
    return config, reducer_config_list, strings_extract
