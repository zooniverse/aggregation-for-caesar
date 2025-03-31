from collections import OrderedDict, defaultdict
from multiprocessing import Pool
import copy
import numpy as np
import os
import json
import progressbar
import pandas
from panoptes_aggregation import extractors
from panoptes_aggregation import reducers
from panoptes_aggregation.csv_utils import flatten_data, unflatten_data
from panoptes_aggregation.extractors.utilities import annotation_by_task


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


def batch_extract(
    classifications,
    extractor_config,
    cpu_count=1,
    verbose=False,
    hide_progressbar=False
):
    '''
        Extracts the values given a list of classifications and a corresponding
        set of extractors

        Inputs
        ------
        classifications: pandas.DataFrame
            A pandas DataFrame with the following columns:
                - classification_id: int
                    ID for the classification on Zooniverse
                - user_name: str
                    Zooniverse user name for person who did the classification
                - user_id: int
                    Zooniverse user ID for the person who did the classification
                - workflow_id: int
                    Zooniverse workflow ID for the classification
                - created_at: str
                    Time of classification
                - subject_ids: int
                    Subject ID for the subject which corresponds to the classification
                - annotations: str
                    A JSON formatted string for the classification output
                - metadata: str
                    A JSON formatted string for the subject metadata
        extractor_config: dict
            A dictionary defining the configuration for the extractor
        cpu_count: int
            The number of CPU cores to be used.
        verbose: bool:
            If True, increase output verbosity.
        hide_progressbar: bool:
            If True, the progress bar is hidden.
    '''
    extracts_data = defaultdict(list)
    if hide_progressbar:
        def callback(name_with_row):
            nonlocal extracts_data  # noqa: F824
            extractor_name, new_extract_row = name_with_row
            if new_extract_row is not None:
                extracts_data[extractor_name] += new_extract_row
    else:
        widgets = [
            'Extracting: ',
            progressbar.Percentage(),
            ' ', progressbar.Bar(),
            ' ', progressbar.ETA()
        ]
        number_of_extractors = sum([len(value) for _, value in extractor_config.items()])
        max_pbar = len(classifications) * number_of_extractors
        pbar = progressbar.ProgressBar(widgets=widgets, max_value=max_pbar)
        counter = 0

        def callback(name_with_row):
            nonlocal extracts_data  # noqa: F824
            nonlocal counter  # noqa: F824
            nonlocal pbar  # noqa: F824
            extractor_name, new_extract_row = name_with_row
            if new_extract_row is not None:
                extracts_data[extractor_name] += new_extract_row
            counter += 1
            pbar.update(counter)

        pbar.start()

    if cpu_count > 1:
        pool = Pool(cpu_count)
    for _, classification in classifications.iterrows():
        classification_by_task = annotation_by_task({
            'annotations': json.loads(classification.annotations),
            'metadata': json.loads(classification.metadata)
        })
        classification_info = {
            'classification_id': classification.classification_id,
            'user_name': classification.user_name,
            'user_id': classification.user_id,
            'workflow_id': classification.workflow_id,
            'created_at': classification.created_at,
            'subject_ids': classification.subject_ids
        }
        for extractor_name, keywords in extractor_config.items():
            extractor_key = extractor_name
            if 'shape_extractor' in extractor_name:
                extractor_key = 'shape_extractor'
            for keyword in keywords:
                if extractor_key in extractors.extractors:
                    if cpu_count > 1:
                        pool.apply_async(
                            extract_classification,
                            args=(
                                copy.deepcopy(classification_by_task),
                                classification_info,
                                extractor_key,
                                extractor_name,
                                keyword,
                                verbose
                            ),
                            callback=callback
                        )
                    else:
                        name_with_row = extract_classification(
                            copy.deepcopy(classification_by_task),
                            classification_info,
                            extractor_key,
                            extractor_name,
                            keyword,
                            verbose
                        )
                        callback(name_with_row)
                else:
                    callback((None, None))
    if cpu_count > 1:
        pool.close()
        pool.join()

    if hide_progressbar is False:
        pbar.finish()

    flat_extracts = defaultdict(list)
    for extractor_name, data in extracts_data.items():
        non_flat_extract = pandas.DataFrame(data)
        flat_extract = flatten_data(non_flat_extract)
        flat_extracts[extractor_name] = flat_extract
    return flat_extracts


def extract_classification(
    classification_by_task,
    classification_info,
    extractor_key,
    extractor_name,
    keyword,
    verbose
):
    try:
        recursive_subject_ids = keyword.get('recursive_subject_ids', False)
        extract = extractors.extractors[extractor_key](classification_by_task, **keyword)
        new_extract_row = []
        if isinstance(extract, list):
            for edx, e in enumerate(extract):
                subject_id = classification_info['subject_ids']
                if recursive_subject_ids:
                    subject_id = f'{subject_id}_{edx}'
                new_extract_row.append(OrderedDict([
                    ('classification_id', classification_info['classification_id']),
                    ('user_name', classification_info['user_name']),
                    ('user_id', classification_info['user_id']),
                    ('workflow_id', classification_info['workflow_id']),
                    ('task', keyword['task']),
                    ('created_at', classification_info['created_at']),
                    ('subject_id', subject_id),
                    ('extractor', extractor_name),
                    ('data', e)
                ]))
        else:
            new_extract_row.append(OrderedDict([
                ('classification_id', classification_info['classification_id']),
                ('user_name', classification_info['user_name']),
                ('user_id', classification_info['user_id']),
                ('workflow_id', classification_info['workflow_id']),
                ('task', keyword['task']),
                ('created_at', classification_info['created_at']),
                ('subject_id', classification_info['subject_ids']),
                ('extractor', extractor_name),
                ('data', extract)
            ]))
    except:
        new_extract_row = None
        if verbose:
            print()
            print('Incorrectly formatted annotation')
            print(classification_info)
            print(extractor_key)
            print(classification_by_task)
    return extractor_name, new_extract_row


def parse_reducer_config(config):
    assert (len(config['reducer_config']) == 1), 'There must be only one reducer in the config file.'
    for key, value in config['reducer_config'].items():
        reducer_name = key
        keywords = value
    assert (reducer_name in reducers.reducers), 'The reducer in the config files does not exist.'
    return reducer_name, keywords


def batch_reduce(
    extracts,
    config,
    cpu_count=1,
    stream=False,
    output_path=None,
    hide_progressbar=False
):
    '''
        Reduces a list of extracts on a per-subject basis and returns an aggregated
        pandas.DataFrame object

        Inputs
        ------
        extracts: pandas.DataFrame
            A pandas DataFrame with the following columns:
                - user_name: str
                    Zooniverse user name for person who did the classification
                - user_id: int
                    Zooniverse user ID for the person who did the classification
                - workflow_id: int
                    Zooniverse workflow ID for the classification
                - created_at: str
                    Time of classification
                - subject_id: int
                    Subject ID for the subject which corresponds to the classification
                - data: str
                    A JSON formatted string for the extracted data
        config: dict
            A dictionary defining the configuration for the reducer
        cpu_count: int
            Number of CPUs to use (1 disables multithreading)
        stream: boolean
            Whether to stream to an output CSV (and resume from the CSV in case of a stopped reduction)
        output_path: str
            Path to output CSV (used only if stream=True)
        hide_progressbar: bool:
            If True, the progress bar is hidden.
    '''
    extracts.sort_values(['subject_id', 'created_at'], inplace=True)
    subjects = extracts.subject_id.unique()
    tasks = extracts.task.unique()
    workflow_id = extracts.workflow_id.iloc[0]

    reducer_name, keywords = parse_reducer_config(config)

    apply_keywords = {
        'reducer_name': reducer_name,
        'workflow_id': workflow_id,
        'filter': filter,
        'keywords': keywords
    }
    if hide_progressbar:
        def callback(reduced_data_list):
            nonlocal reduced_data  # noqa: F824
            nonlocal sdx  # noqa: F824
            nonlocal stream  # noqa: F824
            reduced_data += reduced_data_list
            if (stream) and (output_path is not None):
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
    else:
        widgets = [
            'Reducing: ',
            progressbar.Percentage(),
            ' ', progressbar.Bar(),
            ' ', progressbar.ETA()
        ]
        number_of_rows = len(subjects) * len(tasks)
        pbar = progressbar.ProgressBar(widgets=widgets, max_value=number_of_rows)

        def callback(reduced_data_list):
            nonlocal reduced_data  # noqa: F824
            nonlocal sdx  # noqa: F824
            nonlocal pbar  # noqa: F824
            nonlocal stream  # noqa: F824
            reduced_data += reduced_data_list
            if (stream) and (output_path is not None):
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

    sdx = 0
    resume = False
    if stream:
        if os.path.isfile(output_path):
            print('resuming from last run')
            resume = True
            with open(output_path, 'r', encoding='utf-8') as reduced_file:
                reduced_csv = pandas.read_csv(reduced_file, encoding='utf-8')
                subjects = np.setdiff1d(subjects, reduced_csv.subject_id)

    reduced_data = []

    if cpu_count > 1:
        pool = Pool(cpu_count)
    for subject in subjects:
        idx = extracts.subject_id == subject
        for task in tasks:
            jdx = extracts.task == task
            classifications = extracts[idx & jdx]
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
    if hide_progressbar is False:
        pbar.finish()
    return pandas.DataFrame(reduced_data)


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
    created_at = [c.created_at for cdx, c in classifications.iterrows()]
    reduction = reducers.reducers[reducer_name](data, user_id=user_ids, created_at=created_at, **keywords)
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
