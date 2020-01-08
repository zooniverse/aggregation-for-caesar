#!/usr/bin/env python

import panoptes_aggregation
import argparse
import json
import os
import sys

try:
    from gooey import GooeyParser
except ImportError:  # pragma: no cover
    from .no_gooey import GooeyParser  # pragma: no cover


def main(args=None):
    parser = GooeyParser(
        description="Aggregate panoptes data files"
    )
    subparsers = parser.add_subparsers(dest='subparser')

    config_parser = subparsers.add_parser(
        'config',
        description='Make configuration files for panoptes data extraction and reduction based on a workflow export',
        help='Make configuration files for panoptes data extraction and reduction based on a workflow export'
    )
    config_load_files = config_parser.add_argument_group(
        'Load Workflow Files',
        'This file can be exported from a project\'s Data Export tab',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    config_numbers = config_parser.add_argument_group(
        'Workflow ID and version numbers',
        'Enter the workflow ID, major version number, and minor version number',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    config_keywords = config_parser.add_argument_group(
        'Other keywords',
        'Additional keywords to be passed into the configuration files',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    config_save_files = config_parser.add_argument_group(
        'Save Config Files',
        'The directory to save the configuration files to',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    config_options = config_parser.add_argument_group(
        'Other options',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    config_load_files.add_argument(
        "workflow_csv",
        help="The csv file containing the workflow data",
        type=argparse.FileType('r', encoding='utf-8'),
        widget='FileChooser'
    )
    config_save_files.add_argument(
        "-d",
        "--dir",
        help="The directory to save the configuration files to",
        type=panoptes_aggregation.scripts.PathType(type='dir'),
        default=os.path.abspath('.'),
        widget='DirChooser'
    )
    config_numbers.add_argument(
        "workflow_id",
        help="the workflow ID you would like to extract",
        type=int
    )
    config_numbers.add_argument(
        "-v",
        "--version",
        help="The major workflow version to extract",
        type=int
    )
    config_numbers.add_argument(
        "-m",
        "--minor_version",
        help="The minor workflow version used to create the lookup table for the workflow content",
        type=int
    )
    config_keywords.add_argument(
        "-k",
        "--keywords",
        help="keywords to be passed into the configuration of a task in the form of a json string, e.g. \'{\"T0\": {\"dot_freq\": \"line\"} }\'\n(note: double quotes must be used inside the brackets)",
        type=json.loads,
        default={}
    )
    config_options.add_argument(
        "-vv",
        "--verbose",
        help="increase output verbosity",
        action="store_true"
    )

    extract_parser = subparsers.add_parser(
        'extract',
        description="Extract data from panoptes classifications based on the workflow",
        help="Extract data from panoptes classifications based on the workflow"
    )
    extract_load_files = extract_parser.add_argument_group(
        'Load classification and configuration files',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    extract_save_files = extract_parser.add_argument_group(
        'What directory and base name should be used for the extractions',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    extract_options = extract_parser.add_argument_group(
        'Other options',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    extract_load_files.add_argument(
        "classification_csv",
        help="The classification csv file containing the panoptes data dump",
        type=argparse.FileType('r', encoding='utf-8'),
        widget='FileChooser'
    )
    extract_load_files.add_argument(
        'extractor_config',
        help="The extractor configuration configuration file",
        type=argparse.FileType('r', encoding='utf-8'),
        widget='FileChooser'
    )
    extract_save_files.add_argument(
        "-d",
        "--dir",
        help="The directory to save the extraction file(s) to",
        type=panoptes_aggregation.scripts.PathType(type='dir'),
        default=os.path.abspath('.'),
        widget='DirChooser'
    )
    extract_save_files.add_argument(
        "-o",
        "--output",
        help="The base name for output csv file to store the extractions (one file will be created for each extractor used)",
        type=str,
        default="extractions"
    )
    extract_options.add_argument(
        "-O",
        "--order",
        help="Arrange the data columns in alphabetical order before saving",
        action="store_true"
    )
    extract_options.add_argument(
        "-c",
        "--cpu_count",
        help="How many cpu cores to use during extraction",
        type=int,
        default=1
    )
    extract_options.add_argument(
        "-vv",
        "--verbose",
        help="increase output verbosity",
        action="store_true"
    )

    reduce_parser = subparsers.add_parser(
        'reduce',
        description="reduce data from panoptes classifications based on the extracted data",
        help="reduce data from panoptes classifications based on the extracted data"
    )
    reduce_load_files = reduce_parser.add_argument_group(
        'Load extraction and configuration files',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    reduce_save_files = reduce_parser.add_argument_group(
        'What directory and base name should be used for the reductions',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    reduce_options = reduce_parser.add_argument_group(
        'Reducer options',
        gooey_options={
            'show_border': False,
            'columns': 1
        }
    )
    reduce_load_files.add_argument(
        "extracted_csv",
        help="The extracted csv file",
        type=argparse.FileType('r', encoding='utf-8'),
        widget='FileChooser'
    )
    reduce_load_files.add_argument(
        "reducer_config",
        help="The reducer configuration file",
        type=argparse.FileType('r', encoding='utf-8'),
        widget='FileChooser'
    )
    reduce_options.add_argument(
        "-F",
        "--filter",
        help="How to filter a user making multiple classifications for one subject",
        type=str,
        choices=['first', 'last', 'all'],
        default='first'
    )
    reduce_options.add_argument(
        "-O",
        "--order",
        help="Arrange the data columns in alphabetical order before saving",
        action="store_true"
    )
    reduce_options.add_argument(
        "-c",
        "--cpu_count",
        help="How many cpu cores to use during reduction",
        type=int,
        default=1
    )
    reduce_save_files.add_argument(
        "-d",
        "--dir",
        help="The directory to save the reduction file to",
        type=panoptes_aggregation.scripts.PathType(type='dir'),
        default=os.path.abspath('.'),
        widget='DirChooser'
    )
    reduce_save_files.add_argument(
        "-o",
        "--output",
        help="The base name for output csv file to store the reductions",
        type=str,
        default="reductions",
        widget='DirChooser'
    )
    reduce_save_files.add_argument(
        "-s",
        "--stream",
        help="Stream output to csv after each reduction (this is slower but is resumable)",
        action="store_true"
    )

    args = parser.parse_args(args)
    if args.subparser == 'config':
        panoptes_aggregation.scripts.config_workflow(
            args.workflow_csv,
            args.workflow_id,
            version=args.version,
            minor_version=args.minor_version,
            keywords=args.keywords,
            output_dir=args.dir,
            verbose=args.verbose
        )
    elif args.subparser == 'extract':
        panoptes_aggregation.scripts.extract_csv(
            args.classification_csv,
            args.extractor_config,
            output_name=args.output,
            output_dir=args.dir,
            order=args.order,
            verbose=args.verbose,
            cpu_count=args.cpu_count
        )
    elif args.subparser == 'reduce':
        panoptes_aggregation.scripts.reduce_csv(
            args.extracted_csv,
            args.reducer_config,
            filter=args.filter,
            output_name=args.output,
            output_dir=args.dir,
            order=args.order,
            stream=args.stream,
            cpu_count=args.cpu_count
        )
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
