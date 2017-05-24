#!/usr/bin/env python

import argparse
from panoptes_aggregation import extractors
import json
import pandas
import progressbar

parser = argparse.ArgumentParser(description="extract data from panoptes classifications based on the workflow")
parser.add_argument("classification_csv", help="the classificaiton csv file containing the panoptes data dump", type=str)
parser.add_argument("workflow_csv", help="the csv file containing the workflow data", type=str)
parser.add_argument("workflow_id", help="the workflow ID you would like to extract", type=int)
parser.add_argument("-v", "--version", help="the workflow version to extract", type=int, default=1)
parser.add_argument("-o", "--output", help="the output csv file to store the annotation extractions", type=str, default="extractions.csv")
args = parser.parse_args()

workflows = pandas.read_csv(args.workflow_csv)
wdx = (workflows.workflow_id == args.workflow_id) & (workflows.version == args.version)
if wdx.sum() == 0:
    raise IndexError('workflow ID and workflow version combination does not exist')
if wdx.sum() > 1:
    raise IndexError('workflow ID and workflow version combination is not unique')
workflow = workflows[wdx].iloc[0]
workflow_tasks = json.loads(workflow.tasks)

extractor_config = {}
for task_key, task in workflow_tasks.items():
    # only extracts drawing at the moment
    # this config maps the tool number to the extractor type
    if task['type'] == 'drawing':
        tools_config = {}
        for tdx, tool in enumerate(task['tools']):
            tools_config.setdefault('{0}_extractor'.format(tool['type']), []).append(tdx)
        extractor_config[task_key] = tools_config


def filter_annotations(annotations, config):
    # this is specific to drawing tasks at the moment
    # each tool can use a different extractor
    # this will split the annotations by extractor type
    annotations_by_extractor = {}
    for annotation in annotations:
        if annotation['task'] in config:
            for extractor_name, tool_idx in config[annotation['task']].items():
                extracted_annotation = {'task': annotation['task'], 'value': []}
                for value in annotation['value']:
                    if value['tool'] in tool_idx:
                        extracted_annotation['value'].append(value)
                annotations_by_extractor[extractor_name] = extracted_annotation
    return annotations_by_extractor


extracted_data = {
    "classification_id": [],
    "user_name": [],
    "user_id": [],
    "workflow_id": [],
    "created_at": [],
    "subject_id": [],
    "extractor": [],
    "data": []
}

classifications = pandas.read_csv(args.classification_csv)

widgets = [
    'Extracting: ',
    progressbar.Percentage(),
    ' ', progressbar.Bar(),
    ' ', progressbar.ETA()
]
pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(classifications))
pbar.start()
for cdx, classification in classifications.iterrows():
    annotations_by_extractor = filter_annotations(json.loads(classification.annotations), extractor_config)
    for extractor_name, annotations in annotations_by_extractor.items():
        extract = extractors.extractors_base[extractor_name]({'annotations': [annotations]})
        extracted_data['classification_id'].append(classification.classification_id)
        extracted_data['user_name'].append(classification.user_name)
        extracted_data['user_id'].append(classification.user_id)
        extracted_data['workflow_id'].append(classification.workflow_id)
        extracted_data['created_at'].append(classification.created_at)
        extracted_data['subject_id'].append(classification.subject_ids)
        extracted_data['extractor'].append(extractor_name)
        # This uses a json column for the extracts since multiple extractros
        # can be in the same csv file
        extracted_data['data'].append(json.dumps(extract))
    pbar.update(cdx + 1)
pbar.finish()

pandas.DataFrame(extracted_data).to_csv(args.output, index=False)
