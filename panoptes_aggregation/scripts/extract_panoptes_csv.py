from collections import OrderedDict, defaultdict
from multiprocessing import Pool
import packaging.version
import copy
import json
import io
import yaml
import os
import progressbar
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="Polyfit may be poorly conditioned")

import pandas
from panoptes_aggregation import extractors
from panoptes_aggregation.csv_utils import flatten_data, order_columns
from panoptes_aggregation.extractors.utilities import annotation_by_task


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')  # pragma: no cover
    return file


def extract_classification(
    classification_by_task,
    classification_info,
    extractor_key,
    extractor_name,
    keyword,
    verbose
):
    try:
        extract = extractors.extractors[extractor_key](classification_by_task, **keyword)
        new_extract_row = []
        if isinstance(extract, list):
            for e in extract:
                new_extract_row.append(OrderedDict([
                    ('classification_id', classification_info['classification_id']),
                    ('user_name', classification_info['user_name']),
                    ('user_id', classification_info['user_id']),
                    ('workflow_id', classification_info['workflow_id']),
                    ('task', keyword['task']),
                    ('created_at', classification_info['created_at']),
                    ('subject_id', classification_info['subject_ids']),
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


CURRENT_PATH = os.path.abspath('.')


def extract_csv(
    classification_csv,
    config,
    output_dir=CURRENT_PATH,
    output_name='extractions',
    order=False,
    verbose=False,
    cpu_count=1
):
    config = get_file_instance(config)
    with config as config_in:
        config_yaml = yaml.load(config_in, Loader=yaml.SafeLoader)

    extractor_config = config_yaml['extractor_config']
    workflow_id = config_yaml['workflow_id']
    version = packaging.version.parse(config_yaml['workflow_version'])
    number_of_extractors = sum([len(value) for key, value in extractor_config.items()])

    extracted_data = defaultdict(list)

    classification_csv = get_file_instance(classification_csv)
    with classification_csv as classification_csv_in:
        classifications = pandas.read_csv(classification_csv_in, encoding='utf-8', dtype={'workflow_version': str})

    wdx = classifications.workflow_id == workflow_id
    assert (wdx.sum() > 0), 'There are no classifications matching the configured workflow ID'

    classifications.workflow_version = classifications.workflow_version.apply(packaging.version.parse)
    if version.minor > 0:
        vdx = classifications.workflow_version == version
    else:
        next_version = packaging.version.parse(str(version.major + 1))
        vdx = (classifications.workflow_version >= version) & (classifications.workflow_version < next_version)

    assert (vdx.sum() > 0), 'There are no classifications matching the configured version number'
    assert ((vdx & wdx).sum() > 0), 'There are no classifications matching the combined workflow ID and version number'

    widgets = [
        'Extracting: ',
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA()
    ]
    max_pbar = (wdx & vdx).sum() * number_of_extractors
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=max_pbar)
    counter = 0

    def callback(name_with_row):
        nonlocal extracted_data
        nonlocal counter
        nonlocal pbar
        extractor_name, new_extract_row = name_with_row
        if new_extract_row is not None:
            extracted_data[extractor_name] += new_extract_row
        counter += 1
        pbar.update(counter)

    pbar.start()
    if cpu_count > 1:
        pool = Pool(cpu_count)
    for _, classification in classifications[wdx & vdx].iterrows():
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
    pbar.finish()

    # create one flat csv file for each extractor used
    output_base_name, _ = os.path.splitext(output_name)
    output_files = []
    for extractor_name, data in extracted_data.items():
        output_path = os.path.join(output_dir, '{0}_{1}.csv'.format(extractor_name, output_base_name))
        output_files.append(output_path)
        non_flat_extract = pandas.DataFrame(data)
        flat_extract = flatten_data(non_flat_extract)
        if order:
            flat_extract = order_columns(flat_extract, front=['choice'])
        flat_extract.to_csv(output_path, index=False, encoding='utf-8')
    return output_files
