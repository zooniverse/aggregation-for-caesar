#!/usr/bin/env python

import io
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


def config_workflow(workflow_csv, workflow_id, version=None, keywords={}, workflow_content=None, minor_version=None, language='en'):
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
    with open(filename, 'w', encoding='utf-8') as stream:
        yaml.dump(config, stream=stream, default_flow_style=False, indent=4)
    reducer_config_list = workflow_reducer_config(extractor_config)
    task_set = set({})
    for extractor, reducer in zip(sorted(extractor_config.keys()), reducer_config_list):
        reducer_config = {
            'reducer_config': reducer
        }
        filename = 'Reducer_config_workflow_{0}_V{1}_{2}.yaml'.format(workflow_id, version, extractor)
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(reducer_config, stream=stream, default_flow_style=False, indent=4)
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
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(stirngs_extract, stream=stream, default_flow_style=False, indent=4)
    return config


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Make configuration files for panoptes data extraction and reduction based on a workflow export"
    )
    parser.add_argument(
        "workflow_csv",
        help="the csv file containing the workflow data",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        "workflow_id",
        help="the workflow ID you would like to extract",
        type=int
    )
    parser.add_argument(
        "-v",
        "--version",
        help="The major workflow version to extract",
        type=int
    )
    parser.add_argument(
        "-k",
        "--keywords",
        help="keywords to be passed into the configuration of a task in the form of a json string, e.g. \'{\"T0\": {\"dot_freq\": \"line\"} }\'  (note: double quotes must be used inside the brackets)",
        type=json.loads,
        default={}
    )
    parser.add_argument(
        "-c",
        "--workflow_content",
        help="The (optional) workflow content file can be provided to create a lookup table for task/answer/tool numbers to the text used on the workflow.",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        "-m",
        "--minor_version",
        help="The minor workflow version used to create the lookup table for the workflow content",
        type=int
    )
    parser.add_argument(
        "-l",
        "--language",
        help="The language to use for the workflow content",
        type=str,
        default='en'
    )
    args = parser.parse_args()

    config_workflow(
        args.workflow_csv,
        args.workflow_id,
        version=args.version,
        keywords=args.keywords,
        workflow_content=args.workflow_content,
        minor_version=args.minor_version,
        language=args.language
    )


if __name__ == "__main__":
    main()
