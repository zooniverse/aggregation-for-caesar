from .batch_utils import batch_reduce, parse_reducer_config
from panoptes_aggregation.csv_utils import flatten_data, order_columns
import pandas
import io
import os
import yaml
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')  # pragma: no cover
    return file


CURRENT_PATH = os.path.abspath('.')


def reduce_csv(
    extracted_csv,
    reducer_config,
    filter='first',
    output_name='reductions',
    output_dir=CURRENT_PATH,
    order=False,
    stream=False,
    cpu_count=1,
    hide_progressbar=False
):
    extracted_csv = get_file_instance(extracted_csv)
    with extracted_csv as extracted_csv_in:
        extracted = pandas.read_csv(
            extracted_csv_in,
            parse_dates=['created_at'],
            encoding='utf-8'
        )

    reducer_config = get_file_instance(reducer_config)
    with reducer_config as config:
        config_yaml = yaml.load(config, Loader=yaml.SafeLoader)

    reducer_name, _ = parse_reducer_config(config_yaml)

    output_base_name, _ = os.path.splitext(output_name)
    output_path = os.path.join(output_dir, '{0}_{1}.csv'.format(reducer_name, output_base_name))

    non_flat_data = batch_reduce(extracted, config_yaml, cpu_count=cpu_count,
                                 stream=stream, output_path=output_path,
                                 hide_progressbar=hide_progressbar)
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
        flat_reduced_data = flatten_data(non_flat_data)
    if order:
        flat_reduced_data = order_columns(flat_reduced_data, front=['choice', 'total_vote_count', 'choice_count'])
    flat_reduced_data.to_csv(output_path, index=False, encoding='utf-8')
    return output_path
