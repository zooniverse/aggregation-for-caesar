import numpy as np
import packaging.version
import io
import yaml
import os
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="Polyfit may be poorly conditioned")

import pandas
from .batch_utils import batch_extract
from panoptes_aggregation.csv_utils import order_columns


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')  # pragma: no cover
    return file


CURRENT_PATH = os.path.abspath('.')


def extract_csv(
    classification_csv,
    config,
    output_dir=CURRENT_PATH,
    output_name='extractions',
    order=False,
    verbose=False,
    cpu_count=1,
    hide_progressbar=False
):
    config = get_file_instance(config)
    with config as config_in:
        config_yaml = yaml.load(config_in, Loader=yaml.SafeLoader)

    extractor_config = config_yaml['extractor_config']
    workflow_id = config_yaml['workflow_id']
    if isinstance(config_yaml['workflow_version'], dict):
        # a version range was given
        version_range = config_yaml['workflow_version']
        for key, value in version_range.items():
            version_range[key] = packaging.version.parse(value)
            # If the max version is only given as a major version, then bump it up to the next largest
            # major version, with minor version 0, so that the <= query will correctly include anything
            # with a major version number matching the max
            if key == 'max' and version_range[key].minor == 0:
                version_range[key] = packaging.version.parse(str(version_range[key].major + 1))
    else:
        # a single version is given
        version = packaging.version.parse(config_yaml['workflow_version'])
        if version.minor == 0:
            # only a major version given, take all rows with the same major version
            # note, the max is inclusive, but there are no workflows with a minor
            # version of 0, so that is OK here
            next_version = packaging.version.parse(str(version.major + 1))
        else:
            next_version = version
        version_range = {
            'min': version,
            'max': next_version
        }

    classification_csv = get_file_instance(classification_csv)
    with classification_csv as classification_csv_in:
        classifications = pandas.read_csv(classification_csv_in, encoding='utf-8', dtype={'workflow_version': str})

    wdx = classifications.workflow_id == workflow_id
    assert (wdx.sum() > 0), 'There are no classifications matching the configured workflow ID'

    classifications.workflow_version = classifications.workflow_version.apply(packaging.version.parse)
    vdx = np.ones_like(classifications.workflow_version, dtype=bool)
    if 'min' in version_range:
        vdx &= classifications.workflow_version >= version_range['min']
    if 'max' in version_range:
        vdx &= classifications.workflow_version <= version_range['max']

    assert (vdx.sum() > 0), 'There are no classifications matching the configured version number(s)'
    assert ((vdx & wdx).sum() > 0), 'There are no classifications matching the combined workflow ID and version number(s)'

    extracted_data = batch_extract(classifications[vdx & wdx], extractor_config, cpu_count, verbose, hide_progressbar=hide_progressbar)

    # create one flat csv file for each extractor used
    output_base_name, _ = os.path.splitext(output_name)
    output_files = []
    for extractor_name, flat_extract in extracted_data.items():
        output_path = os.path.join(output_dir, '{0}_{1}.csv'.format(extractor_name, output_base_name))
        output_files.append(output_path)
        if order:
            flat_extract = order_columns(flat_extract, front=['choice'])
        flat_extract.to_csv(output_path, index=False, encoding='utf-8')
    return output_files
