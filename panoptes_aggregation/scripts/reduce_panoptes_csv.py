#!/usr/bin/env python

from collections import OrderedDict
import copy
import io
import os
import progressbar
import yaml
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import numpy as np
import pandas
from panoptes_aggregation import reducers
from panoptes_aggregation.csv_utils import flatten_data, unflatten_data, order_columns


def first_filter(data):
    first_time = data.created_at.min()
    fdx = data.created_at == first_time
    return data[fdx]


def last_filter(data):
    last_time = data.created_at.max()
    ldx = data.created_at == last_time
    return data[ldx]


FILTER_TYPES = {
    'first': first_filter,
    'last': last_filter
}


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')
    return file


def reduce_csv(extracted_csv, reducer_config, filter='first', output='reductions', order=False, stream=False):
    extracted_csv = get_file_instance(extracted_csv)
    with extracted_csv as extracted_csv_in:
        extracted = pandas.read_csv(extracted_csv_in, infer_datetime_format=True, parse_dates=['created_at'], encoding='utf-8')

    extracted.sort_values(['subject_id', 'created_at'], inplace=True)
    resume = False
    subjects = extracted.subject_id.unique()
    tasks = extracted.task.unique()
    workflow_id = extracted.workflow_id.iloc[0]

    reducer_config = get_file_instance(reducer_config)
    with reducer_config as config:
        config_yaml = yaml.load(config)

    assert (len(config_yaml['reducer_config']) == 1), 'There must be only one reducer in the config file.'
    for key, value in config_yaml['reducer_config'].items():
        reducer_name = key
        keywords = value
    assert (reducer_name in reducers.reducers), 'The reducer in the config files does not exist.'

    output_path, output_base = os.path.split(output)
    output_base_name, output_ext = os.path.splitext(output_base)
    output_name = os.path.join(output_path, '{0}_{1}.csv'.format(reducer_name, output_base_name))

    if stream:
        if os.path.isfile(output_name):
            print('resuming from last run')
            resume = True
            with open(output_name, 'r', encoding='utf-8') as reduced_file:
                reduced_csv = pandas.read_csv(reduced_file, encoding='utf-8')
                subjects = np.setdiff1d(subjects, reduced_csv.subject_id)

    blank_reduced_data = OrderedDict([
        ('subject_id', []),
        ('workflow_id', []),
        ('task', []),
        ('reducer', []),
        ('data', [])
    ])

    reduced_data = copy.deepcopy(blank_reduced_data)

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
            classifications = classifications.drop_duplicates()
            if filter in FILTER_TYPES:
                classifications = classifications.groupby(['user_name'], group_keys=False).apply(FILTER_TYPES[filter])
            data = [unflatten_data(c) for cdx, c in classifications.iterrows()]
            reduction = reducers.reducers[reducer_name](data, **keywords)
            if isinstance(reduction, list):
                for r in reduction:
                    reduced_data['subject_id'].append(subject)
                    reduced_data['workflow_id'].append(workflow_id)
                    reduced_data['task'].append(task)
                    reduced_data['reducer'].append(reducer_name)
                    reduced_data['data'].append(r)
            else:
                reduced_data['subject_id'].append(subject)
                reduced_data['workflow_id'].append(workflow_id)
                reduced_data['task'].append(task)
                reduced_data['reducer'].append(reducer_name)
                reduced_data['data'].append(reduction)
        if stream:
            if (sdx == 0) and (not resume):
                pandas.DataFrame(reduced_data).to_csv(output_name, mode='w', index=False, encoding='utf-8')
            else:
                pandas.DataFrame(reduced_data).to_csv(output_name, mode='a', index=False, header=False, encoding='utf-8')
            reduced_data = copy.deepcopy(blank_reduced_data)
        pbar.update(sdx + 1)
    pbar.finish()

    if stream:
        reduced_csv = pandas.read_csv(output_name, encoding='utf-8')
        if 'data' in reduced_csv:
            reduced_csv.data = reduced_csv.data.apply(eval)
            flat_reduced_data = flatten_data(reduced_csv)
        else:
            return output_name
    else:
        flat_reduced_data = flatten_data(reduced_data)
    if order:
        flat_reduced_data = order_columns(flat_reduced_data, front=['choice', 'total_vote_count', 'choice_count'])
    flat_reduced_data.to_csv(output_name, index=False, encoding='utf-8')
    return output_name


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="reduce data from panoptes classifications based on the extracted data (see extract_panoptes_csv)"
    )
    parser.add_argument(
        "extracted_csv",
        help="the extracted csv file output from extract_panoptes_csv",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        "reducer_config",
        help="the reducer yaml file output from config_workflow_panoptes",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        "-F",
        "--filter",
        help="how to filter a user making multiple classifications for one subject",
        type=str,
        choices=['first', 'last', 'all'],
        default='fisrt'
    )
    parser.add_argument(
        "-O",
        "--order",
        help="arrange the data columns in alphabetical order before saving",
        action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="the base name for output csv file to store the reductions",
        type=str,
        default="reductions"
    )
    parser.add_argument(
        "-s",
        "--stream",
        help="stream output to csv after each reduction (this is slower but is resumable)",
        action="store_true"
    )
    args = parser.parse_args()

    reduce_csv(
        args.extracted_csv,
        args.reducer_config,
        filter=args.filter,
        output=args.output,
        order=args.order,
        stream=args.stream
    )


if __name__ == "__main__":
    main()
