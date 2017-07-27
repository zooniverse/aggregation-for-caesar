#!/usr/bin/env python

from collections import OrderedDict
import copy
from panoptes_aggregation import extractors
from panoptes_aggregation.csv_utils import flatten_data, order_columns
import json
import math
import io
import os
import pandas
import progressbar
import warnings


def extract_csv(classification_csv, workflow_csv, workflow_id, version=None, human=False, output='extractions', order=False):
    if not isinstance(workflow_csv, io.IOBase):
        workflow_csv = open(workflow_csv, 'r')

    with workflow_csv as workflow_csv_in:
        workflows = pandas.read_csv(workflow_csv_in)

    if version is None:
        version = workflow.version.max()
        warnings.warn('No workflow version was specified, defaulting to version {0}'.format(version))

    wdx = (workflows.workflow_id == workflow_id) & (workflows.version == version)
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
        ('task', []),
        ('created_at', []),
        ('subject_id', []),
        ('extractor', []),
        ('data', [])
    ])

    extracted_data = {}

    with classification_csv as classification_csv_in:
        classifications = pandas.read_csv(classification_csv_in)

    widgets = [
        'Extracting: ',
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA()
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(classifications))
    pbar.start()
    for cdx, classification in classifications.iterrows():
        if (classification.workflow_id != workflow_id) or (math.floor(classification.workflow_version) != version):
            pbar.update(cdx + 1)
            continue
        annotations_by_extractor = extractors.filter_annotations(json.loads(classification.annotations), extractor_config, human=human)
        for extractor_name, annotations_list in annotations_by_extractor.items():
            for annotations in annotations_list:
                if extractor_name in extractors.extractors_base:
                    extract = extractors.extractors_base[extractor_name]({'annotations': [annotations]})
                    if isinstance(extract, list):
                        for e in extract:
                            extracted_data.setdefault(extractor_name, copy.deepcopy(blank_extracted_data))
                            extracted_data[extractor_name]['classification_id'].append(classification.classification_id)
                            extracted_data[extractor_name]['user_name'].append(classification.user_name)
                            extracted_data[extractor_name]['user_id'].append(classification.user_id)
                            extracted_data[extractor_name]['workflow_id'].append(classification.workflow_id)
                            extracted_data[extractor_name]['task'].append(annotations['task'])
                            extracted_data[extractor_name]['created_at'].append(classification.created_at)
                            extracted_data[extractor_name]['subject_id'].append(classification.subject_ids)
                            extracted_data[extractor_name]['extractor'].append(extractor_name)
                            extracted_data[extractor_name]['data'].append(e)
                    else:
                        extracted_data.setdefault(extractor_name, copy.deepcopy(blank_extracted_data))
                        extracted_data[extractor_name]['classification_id'].append(classification.classification_id)
                        extracted_data[extractor_name]['user_name'].append(classification.user_name)
                        extracted_data[extractor_name]['user_id'].append(classification.user_id)
                        extracted_data[extractor_name]['workflow_id'].append(classification.workflow_id)
                        extracted_data[extractor_name]['task'].append(annotations['task'])
                        extracted_data[extractor_name]['created_at'].append(classification.created_at)
                        extracted_data[extractor_name]['subject_id'].append(classification.subject_ids)
                        extracted_data[extractor_name]['extractor'].append(extractor_name)
                        extracted_data[extractor_name]['data'].append(extract)
        pbar.update(cdx + 1)
    pbar.finish()

    # create one flat csv file for each extractor used
    output_path, output_base = os.path.split(output)
    output_base_name, output_ext = os.path.splitext(output_base)
    output_files = []
    for extractor_name, data in extracted_data.items():
        if len(data['data']) == 0:
            warnings.warn('No data extracted with {0}'.format(extractor_name))
        output_name = os.path.join(output_path, '{0}_{1}.csv'.format(extractor_name, output_base_name))
        output_files.append(output_name)
        flat_extract = flatten_data(data)
        if order:
            flat_extract = order_columns(flat_extract, front=['choice'])
        flat_extract.to_csv(output_name, index=False)
    return output_files


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="extract data from panoptes classifications based on the workflow")
    parser.add_argument("classification_csv", help="the classificaiton csv file containing the panoptes data dump", type=argparse.FileType('r'))
    parser.add_argument("workflow_csv", help="the csv file containing the workflow data", type=argparse.FileType('r'))
    parser.add_argument("workflow_id", help="the workflow ID you would like to extract", type=int)
    parser.add_argument("-v", "--version", help="the workflow version to extract", type=int)
    parser.add_argument("-H", "--human", help="switch to make the data column labels use the task and question labels instead of generic labels", action="store_true")
    parser.add_argument("-O", "--order", help="arrange the data columns in alphabetical order before saving", action="store_true")
    parser.add_argument("-o", "--output", help="the base name for output csv file to store the annotation extractions (one file will be created for each extractor used)", type=str, default="extractions")
    args = parser.parse_args()

    extract_csv(args.classification_csv, args.workflow_csv, args.workflow_id, version=args.version, human=args.human, output=args.output, order=args.order)
