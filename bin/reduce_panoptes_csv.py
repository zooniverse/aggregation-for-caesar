#!/usr/bin/env python

from collections import OrderedDict
import copy
from panoptes_aggregation import reducers
from panoptes_aggregation.csv_utils import flatten_data, unflatten_data
import json
import math
import io
import os
import pandas
import progressbar


def first_filter(data):
    first_time = data.created_at.min()
    fdx = data.created_at == first_time
    return data[fdx]


def last_filter(data):
    last_time = data.created_at.max()
    ldx = data.created_at == last_time
    return data[ldx]


def reduce_csv(extracted_csv, filter='first', keywords={}, output='reductions'):
    if not isinstance(extracted_csv, io.IOBase):
        extracted_csv = open(extracted_csv, 'r')

    with extracted_csv as extracted_csv_in:
        extracted = pandas.read_csv(extracted_csv_in, infer_datetime_format=True, parse_dates=['created_at'])

    extracted.sort_values(['subject_id', 'created_at'], inplace=True)

    subjects = extracted.subject_id.unique()
    tasks = extracted.task.unique()
    workflow_id = extracted.workflow_id.iloc[0]
    extractor_name = extracted.extractor.iloc[0]
    reducer_name = extractor_name.replace('extractor', 'reducer')

    reduced_data = OrderedDict([
        ('subject_id', []),
        ('workflow_id', []),
        ('task', []),
        ('reducer', []),
        ('data', [])
    ])

    widgets = [
        'Reducing: ',
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA()
    ]

    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(subjects))
    pbar.start()
    for sdx, subject in enumerate(subjects):
        idx = extracted.subject_id == subject
        for task in tasks:
            jdx = extracted.task == task
            classifications = extracted[idx & jdx]
            if filter == 'first':
                classifications = classifications.groupby(['user_name'], group_keys=False).apply(first_filter)
            elif filter == 'last':
                classifications = classifications.groupby(['user_name'], group_keys=False).apply(last_filter)
            classifications.drop_duplicates(inplace=True)
            data = [unflatten_data(c) for cdx, c in classifications.iterrows()]
            reduced_data['subject_id'].append(subject)
            reduced_data['workflow_id'].append(workflow_id)
            reduced_data['task'].append(task)
            reduced_data['reducer'].append(reducer_name)
            reduced_data['data'].append(reducers.reducer_base[reducer_name](data, **keywords))
        pbar.update(sdx + 1)
    pbar.finish()

    output_path, output_base = os.path.split(output)
    ouput_base_name, output_ext = os.path.splitext(output_base)
    output_name = os.path.join(output_path, '{0}_{1}.csv'.format(reducer_name, ouput_base_name))
    flat_reduced_data = flatten_data(reduced_data)
    flat_reduced_data.to_csv(output_name, index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="reduce data from panoptes classifications based on the extracted data (see extract_panoptes_csv)")
    parser.add_argument("extracted_csv", help="the extracted csv file output from extract_panoptes_csv", type=argparse.FileType('r'))
    parser.add_argument("-F", "--filter", help="how to filter a user makeing multiple classifications for one subject", type=str, choices=['first', 'last', 'all'], default='fisrt')
    parser.add_argument("-k", "--keywords", help="keywords to be passed into the reducer in the form of a json string, e.g. \'{\"eps\": 5.5, \"min_samples\": 3}\'  (note: double quotes must be used inside the brackets)", type=json.loads, default={})
    parser.add_argument("-o", "--output", help="the base name for output csv file to store the reductions", type=str, default="reductions")
    args = parser.parse_args()

    reduce_csv(args.extracted_csv, filter=args.filter, keywords=args.keywords, output=args.output)
