import unittest
from unittest.mock import patch
import panoptes_aggregation.scripts
import panoptes_aggregation.scripts.aggregation_parser
import os


class TestAggregationParser(unittest.TestCase):
    @patch('panoptes_aggregation.scripts.aggregation_parser.argparse.FileType')
    @patch('panoptes_aggregation.scripts.config_workflow')
    def test_config_called(self, mock_config_workflow, mock_FileType):
        '''Test panoptes_aggregation config calls config_workflow once'''
        panoptes_aggregation.scripts.parser_main(['config', 'file_in', '123'])
        mock_config_workflow.assert_called_once_with(
            mock_FileType.return_value.return_value,
            123,
            keywords={},
            minor_version=None,
            version=None,
            output_dir=os.getcwd(),
            verbose=False
        )

    @patch('panoptes_aggregation.scripts.aggregation_parser.argparse.FileType')
    @patch('panoptes_aggregation.scripts.extract_csv')
    def test_extract_called(self, mock_extract_csv, mock_FileType):
        '''Test panoptes_aggregation extract calls extract_csv once'''
        panoptes_aggregation.scripts.parser_main(['extract', 'file_in_1', 'file_in_2'])
        mock_extract_csv.assert_called_once_with(
            mock_FileType.return_value.return_value,
            mock_FileType.return_value.return_value,
            order=False,
            output_dir=os.getcwd(),
            verbose=False,
            output_name='extractions'
        )

    @patch('panoptes_aggregation.scripts.aggregation_parser.argparse.FileType')
    @patch('panoptes_aggregation.scripts.reduce_csv')
    def test_reduce_called(self, mock_reduce_csv, mock_FileType):
        '''Test panoptes_aggregation reduce calls reduce_csv once'''
        panoptes_aggregation.scripts.parser_main(['reduce', 'file_in_1', 'file_in_2'])
        mock_reduce_csv.assert_called_once_with(
            mock_FileType.return_value.return_value,
            mock_FileType.return_value.return_value,
            filter='first',
            order=False,
            output_dir=os.getcwd(),
            stream=False,
            output_name='reductions'
        )
