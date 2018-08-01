#!/usr/bin/env python

import io
from panoptes_aggregation import extractors
import pandas
import yaml
import json
import warnings

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
    'sw_variant_extractor': 'sw_variant_reducer'
}


def config_workflow(workflow_csv, workflow_id, version=None, keywords={}):
    if not isinstance(workflow_csv, io.IOBase):
        workflow_csv = open(workflow_csv, 'r', encoding='utf-8')

    with workflow_csv as workflow_csv_in:
        workflows = pandas.read_csv(workflow_csv_in, encoding='utf-8')

    if version is None:
        version = workflows[workflows.workflow_id == workflow_id].version.max()
        warnings.warn('No workflow version was specified, defaulting to version {0}'.format(version))

    wdx = (workflows.workflow_id == workflow_id) & (workflows.version == version)
    if wdx.sum() == 0:
        raise IndexError('workflow ID and workflow version combination does not exist')
    if wdx.sum() > 1:
        raise IndexError('workflow ID and workflow version combination is not unique')
    workflow = workflows[wdx].iloc[0]
    workflow_tasks = json.loads(workflow.tasks)
    extractor_config = extractors.workflow_extractor_config(workflow_tasks, keywords=keywords)
    config = {
        'workflow_id': workflow_id,
        'workflow_version': int(version),
        'extractor_config': extractor_config
    }
    filename = 'Extractor_config_workflow_{0}_V{1}.yaml'.format(workflow_id, version)
    with open(filename, 'w', encoding='utf-8') as stream:
        yaml.dump(config, stream=stream, default_flow_style=False)
    for extractor in extractor_config.keys():
        reducer_config = {
            'reducer_config': {
                standard_reducers[extractor]: {}
            }
        }
        filename = 'Reducer_config_workflow_{0}_V{1}_{2}.yaml'.format(workflow_id, version, extractor)
        with open(filename, 'w', encoding='utf-8') as stream:
            yaml.dump(reducer_config, stream=stream, default_flow_style=False)
    return config


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Make configuation files for panoptes data extraction and reduction based on a workflow export"
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
        help="the workflow version to extract",
        type=int
    )
    parser.add_argument(
        "-k",
        "--keywords",
        help="keywords to be passed into the extractor for a task in the form of a json string, e.g. \'{\"T0\": {\"dot_freq\": \"line\"} }\'  (note: double quotes must be used inside the brackets)",
        type=json.loads,
        default={}
    )
    args = parser.parse_args()

    config_workflow(
        args.workflow_csv,
        args.workflow_id,
        version=args.version,
        keywords=args.keywords
    )
