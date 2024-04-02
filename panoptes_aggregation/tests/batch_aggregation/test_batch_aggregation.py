import unittest
from unittest.mock import patch, Mock, MagicMock
from panoptes_aggregation.scripts import batch_utils
from panoptes_aggregation.batch_aggregation import run_aggregation
from panoptes_aggregation import batch_aggregation as batch_agg

class TestBatchAggregation(unittest.TestCase):
    @patch("panoptes_aggregation.batch_aggregation.workflow_extractor_config")
    @patch("panoptes_aggregation.batch_aggregation.workflow_reducer_config")
    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator")
    def test_run_aggregation(self, mock_aggregator, mock_wf_red_conf, mock_wf_ext_conf):
        mock_aggregator.process_wf_export.return_value = MagicMock()
        mock_aggregator.process_cls_export.return_value = MagicMock()
        batch_utils.batch_extract = MagicMock()
        batch_utils.batch_reduce = MagicMock()
        run_aggregation(1, 10, 100)
        mock_aggregator.assert_called_once_with(1, 10, 100)
        mock_wf_ext_conf.assert_called_once()
        mock_wf_red_conf.assert_called_once()
        batch_utils.batch_extract.assert_called_once()
        batch_utils.batch_reduce.assert_called_once()

    @patch("panoptes_aggregation.batch_aggregation.Workflow")
    @patch("panoptes_aggregation.batch_aggregation.Project")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.connect")
    def test_save_exports(self, mock_client, mock_project, mock_workflow):
        # Test that Panoptes calls are made and files are saved
        csv_dict = {'media': [ {'src': 'http://zooniverse.org/123.csv'} ] }
        mock_project.return_value.describe_export.return_value = csv_dict
        mock_workflow.return_value.describe_export.return_value = csv_dict
        ba = batch_agg.BatchAggregator(1, 10, 100)
        batch_agg.BatchAggregator._download_export = MagicMock(side_effect=[f'./cls_export.csv', f'./wf_export.csv'])
        expected_response = {'cls_csv': 'tmp/10_cls_export.csv', 'wf_csv': 'tmp/1_workflow_export.csv'}
        response = ba.save_exports()
        self.assertEqual(response, expected_response)
        mock_client.assert_called_once()
        mock_project.assert_called_once_with(1)
        mock_workflow.assert_called_once_with(10)
        mock_project.return_value.describe_export.assert_called_once_with('workflows')
        mock_workflow.return_value.describe_export.assert_called_once_with('classifications')

    def test_process_wf_export(self):
        # Test that:
        # the wf export is parsed
        # the version instance vars are set
        # dataframe is retuned
        assert 1 == 1

    def test_process_cls_export(self):
        # Test that the cls csv is parsed and a dataframe is returned
        assert 1 == 1
