from collections import OrderedDict
from multiprocessing import Pool
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
        file = open(file, 'r', encoding='utf-8')  # pragma: no cover
    return file


def reduce_subject(
    subject,
    classifications,
    task,
    reducer_name=None,
    workflow_id=None,
    filter=None,
    keywords={}
):
    reduced_data_list = []
    classifications = classifications.drop_duplicates()
    unique_users = classifications['user_name'].unique().shape[0]
    if (filter in FILTER_TYPES) and (unique_users < classifications.shape[0]):
        classifications = classifications.groupby(['user_name'], group_keys=False).apply(FILTER_TYPES[filter])
    data = [unflatten_data(c) for cdx, c in classifications.iterrows()]
    user_ids = [c.user_id for cdx, c in classifications.iterrows()]
    reduction = reducers.reducers[reducer_name](data, user_id=user_ids, **keywords)
    if isinstance(reduction, list):
        for r in reduction:
            reduced_data_list.append(OrderedDict([
                ('subject_id', subject),
                ('workflow_id', workflow_id),
                ('task', task),
                ('reducer', reducer_name),
                ('data', r)
            ]))
    else:
        reduced_data_list.append(OrderedDict([
            ('subject_id', subject),
            ('workflow_id', workflow_id),
            ('task', task),
            ('reducer', reducer_name),
            ('data', reduction)
        ]))
    return reduced_data_list


CURRENT_PATH = os.path.abspath('.')


def reduce_csv(
    extracted_csv,
    reducer_config,
    filter='first',
    output_name='reductions',
    output_dir=CURRENT_PATH,
    order=False,
    stream=False,
    cpu_count=1
):
    extracted_csv = get_file_instance(extracted_csv)
    with extracted_csv as extracted_csv_in:
        extracted = pandas.read_csv(
            extracted_csv_in,
            infer_datetime_format=True,
            parse_dates=['created_at'],
            encoding='utf-8'
        )

    extracted.sort_values(['subject_id', 'created_at'], inplace=True)
    resume = False
    subjects = extracted.subject_id.unique()
    tasks = extracted.task.unique()
    workflow_id = extracted.workflow_id.iloc[0]

    reducer_config = get_file_instance(reducer_config)
    with reducer_config as config:
        config_yaml = yaml.load(config, Loader=yaml.SafeLoader)

    assert (len(config_yaml['reducer_config']) == 1), 'There must be only one reducer in the config file.'
    for key, value in config_yaml['reducer_config'].items():
        reducer_name = key
        keywords = value
    assert (reducer_name in reducers.reducers), 'The reducer in the config files does not exist.'

    output_base_name, _ = os.path.splitext(output_name)
    output_path = os.path.join(output_dir, '{0}_{1}.csv'.format(reducer_name, output_base_name))

    if stream:
        if os.path.isfile(output_path):
            print('resuming from last run')
            resume = True
            with open(output_path, 'r', encoding='utf-8') as reduced_file:
                reduced_csv = pandas.read_csv(reduced_file, encoding='utf-8')
                subjects = np.setdiff1d(subjects, reduced_csv.subject_id)

    reduced_data = []
    sdx = 0

    apply_keywords = {
        'reducer_name': reducer_name,
        'workflow_id': workflow_id,
        'filter': filter,
        'keywords': keywords
    }

    widgets = [
        'Reducing: ',
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA()
    ]
    number_of_rows = len(subjects) * len(tasks)
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=number_of_rows)

    def callback(reduced_data_list):
        nonlocal reduced_data
        nonlocal sdx
        nonlocal pbar
        nonlocal stream
        reduced_data += reduced_data_list
        if stream:
            if (sdx == 0) and (not resume):
                pandas.DataFrame(reduced_data).to_csv(
                    output_path,
                    mode='w',
                    index=False,
                    encoding='utf-8'
                )
            else:
                pandas.DataFrame(reduced_data).to_csv(
                    output_path,
                    mode='a',
                    index=False,
                    header=False,
                    encoding='utf-8'
                )
            reduced_data.clear()
        sdx += 1
        pbar.update(sdx)

    pbar.start()
    if cpu_count > 1:
        pool = Pool(cpu_count)
    for subject in subjects:
        idx = extracted.subject_id == subject
        for task in tasks:
            jdx = extracted.task == task
            classifications = extracted[idx & jdx]
            if cpu_count > 1:
                pool.apply_async(
                    reduce_subject,
                    args=(
                        subject,
                        classifications,
                        task
                    ),
                    kwds=apply_keywords,
                    callback=callback
                )
            else:
                reduced_data_list = reduce_subject(
                    subject,
                    classifications,
                    task,
                    **apply_keywords
                )
                callback(reduced_data_list)
    if cpu_count > 1:
        pool.close()
        pool.join()
    pbar.finish()

    if stream:
        reduced_csv = pandas.read_csv(output_path, encoding='utf-8')
        if 'data' in reduced_csv:
            def eval_func(a):
                # pandas uses a local namespace, make sure it has the correct imports
                from collections import OrderedDict  # noqa
                from numpy import nan  # noqa
                return eval(a)
            reduced_csv.data = reduced_csv.data.apply(eval_func)
            flat_reduced_data = flatten_data(reduced_csv)
        else:
            return output_path
    else:
        non_flat_data = pandas.DataFrame(reduced_data)
        flat_reduced_data = flatten_data(non_flat_data)
    if order:
        flat_reduced_data = order_columns(flat_reduced_data, front=['choice', 'total_vote_count', 'choice_count'])
    flat_reduced_data.to_csv(output_path, index=False, encoding='utf-8')
    return output_path
