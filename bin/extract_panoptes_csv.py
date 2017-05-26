#!/usr/bin/env python

import argparse
from collections import OrderedDict
import copy
from panoptes_aggregation import extractors
from panoptes_aggregation.flatten_data import flatten_data
import json
import math
import pandas
import progressbar

parser = argparse.ArgumentParser(description="extract data from panoptes classifications based on the workflow")
parser.add_argument("classification_csv", help="the classificaiton csv file containing the panoptes data dump", type=str)
parser.add_argument("workflow_csv", help="the csv file containing the workflow data", type=str)
parser.add_argument("workflow_id", help="the workflow ID you would like to extract", type=int)
parser.add_argument("-v", "--version", help="the workflow version to extract", type=int, default=1)
parser.add_argument("-H", "--human", help="switch to make the data column labels use the task and question labels instead of generic labels", action="store_true")
parser.add_argument("-o", "--output", help="the base name for output csv file to store the annotation extractions (one file will be created for each extractor used)", type=str, default="extractions.csv")
args = parser.parse_args()

workflows = pandas.read_csv(args.workflow_csv)
wdx = (workflows.workflow_id == args.workflow_id) & (workflows.version == args.version)
if wdx.sum() == 0:
    raise IndexError('workflow ID and workflow version combination does not exist')
if wdx.sum() > 1:
    raise IndexError('workflow ID and workflow version combination is not unique')
workflow = workflows[wdx].iloc[0]
workflow_tasks = json.loads(workflow.tasks)
extractor_config = extractors.workflow_extractor_config(workflow_tasks)

blank_extracted_data = OrderedDict([
    ('classification_id', []),
    ('user_name', []),
    ('user_id', []),
    ('workflow_id', []),
    ('created_at', []),
    ('subject_id', []),
    ('extractor', []),
    ('data', [])
])

extracted_data = {}

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
    if (classification.workflow_id != args.workflow_id) or (math.floor(classification.workflow_version) != args.version):
        pbar.update(cdx + 1)
        continue
    annotations_by_extractor = extractors.filter_annotations(json.loads(classification.annotations), extractor_config, human=args.human)
    for extractor_name, annotations in annotations_by_extractor.items():
        if extractor_name in extractors.extractors_base:
            extract = extractors.extractors_base[extractor_name]({'annotations': [annotations]})
            extracted_data.setdefault(extractor_name, copy.deepcopy(blank_extracted_data))
            extracted_data[extractor_name]['classification_id'].append(classification.classification_id)
            extracted_data[extractor_name]['user_name'].append(classification.user_name)
            extracted_data[extractor_name]['user_id'].append(classification.user_id)
            extracted_data[extractor_name]['workflow_id'].append(classification.workflow_id)
            extracted_data[extractor_name]['created_at'].append(classification.created_at)
            extracted_data[extractor_name]['subject_id'].append(classification.subject_ids)
            extracted_data[extractor_name]['extractor'].append(extractor_name)
            extracted_data[extractor_name]['data'].append(extract)
    pbar.update(cdx + 1)
pbar.finish()

# create one flat csv file for each extractor used
for extractor_name, data in extracted_data.items():
    flat_extract = flatten_data(data)
    flat_extract.to_csv('{0}_{1}'.format(extractor_name, args.output), index=False)
