try:
    from panoptes_aggregation.scripts import batch_utils
    from panoptes_aggregation.batch_aggregation import run_aggregation
    from panoptes_aggregation import batch_aggregation as batch_agg

    batch_agg.celery.conf.update(CELERY_BROKER_URL='memory://')
    batch_agg.celery.conf.update(CELERY_RESULT_BACKEND='cache+memory://')
    OFFLINE = False
except ImportError:
    OFFLINE = True
import unittest
import os
from unittest.mock import patch, MagicMock, call


wf_export = 'panoptes_aggregation/tests/batch_aggregation/wf_export.csv'
cls_export = 'panoptes_aggregation/tests/batch_aggregation/cls_export.csv'


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
@patch("panoptes_aggregation.batch_aggregation.BatchAggregator._connect_api_client", new=MagicMock())
class TestBatchAggregation(unittest.TestCase):
    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator")
    def test_run_aggregation_permission_failure(self, mock_aggregator):
        mock_aggregator_instance = mock_aggregator.return_value
        mock_aggregator_instance.check_permission.return_value = False

        with self.assertRaises(SystemExit):
            run_aggregation(1, 10, 100)
        mock_aggregator_instance.update_panoptes.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.workflow_extractor_config")
    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator")
    def test_run_aggregation_success(self, mock_aggregator, mock_wf_ext_conf):
        mock_aggregator_instance = mock_aggregator.return_value
        mock_aggregator_instance.check_permission.return_value = True

        mock_df = MagicMock()
        test_extracts = {'question_extractor': mock_df}
        batch_utils.batch_extract = MagicMock(return_value=test_extracts)
        mock_reducer = MagicMock()
        batch_utils.batch_reduce = mock_reducer

        run_aggregation(1, 10, 100)
        mock_aggregator_instance.check_permission.assert_called_once()
        mock_aggregator.assert_called_once_with(1, 10, 100)
        mock_wf_ext_conf.assert_called_once()
        batch_utils.batch_extract.assert_called_once()
        mock_df.to_csv.assert_called()
        batch_utils.batch_reduce.assert_called()
        self.assertEqual(mock_reducer.call_count, 2)
        mock_aggregator_instance.upload_files.assert_called_once()
        mock_aggregator_instance.update_panoptes.assert_called_once()

    @patch("panoptes_aggregation.batch_aggregation.os.makedirs")
    @patch("panoptes_aggregation.batch_aggregation.Workflow")
    @patch("panoptes_aggregation.batch_aggregation.Project")
    def test_save_exports(self, mock_project, mock_workflow, mock_makedirs):
        # Test that Panoptes calls are made and files are saved
        csv_dict = {'media': [{'src': 'http://zooniverse.org/123.csv'}]}
        mock_project.return_value.describe_export.return_value = csv_dict
        mock_workflow.return_value.describe_export.return_value = csv_dict
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.id = 'asdf123asdf'
        batch_agg.BatchAggregator._download_export = MagicMock(side_effect=['./cls_export.csv', './wf_export.csv'])
        expected_response = {'classifications': 'tmp/asdf123asdf/10_cls_export.csv', 'workflows': 'tmp/asdf123asdf/10_workflow_export.csv'}

        response = ba.save_exports()

        assert ba.id is not None
        self.assertEqual(response, expected_response)
        mock_makedirs.assert_called_once()
        mock_project.assert_called_once_with(1)
        mock_workflow.assert_called_once_with(10)
        mock_project.return_value.describe_export.assert_called_once_with('workflows')
        mock_workflow.return_value.describe_export.assert_called_once_with('classifications')

    def test_process_wf_export(self):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        result = ba.process_wf_export(wf_export)
        self.assertEqual(ba.wf_maj_version, 16)
        self.assertEqual(ba.wf_min_version, 55)
        self.assertEqual(ba.workflow_version, '16.55')
        self.assertEqual(result.__class__.__name__, 'DataFrame')

    def test_process_cls_export(self):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.workflow_version = '16.55'
        result = ba.process_cls_export(cls_export)
        self.assertEqual(result.__class__.__name__, 'DataFrame')

    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator.connect_blob_storage")
    @patch("panoptes_aggregation.batch_aggregation.make_archive")
    def test_upload_files(self, archive_mock, client_mock):
        zipped_mock = MagicMock()
        archive_mock.return_value = zipped_mock
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.upload_file_to_storage = MagicMock()
        ba.output_path = os.path.join('tmp', '10')
        reductions_file = os.path.join('tmp', '10', '10_reductions.csv')
        ba.upload_files()
        client_mock.assert_called_once()
        archive_mock.assert_called_once()
        ba.upload_file_to_storage.assert_has_calls([call(ba.id, reductions_file), call(ba.id, zipped_mock)])

    def test_upload_file_to_storage(self):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        mock_client = MagicMock()
        ba.blob_service_client = MagicMock(return_value=mock_client)
        ba.upload_file_to_storage('container', cls_export)
        mock_client.upload_blob.assert_called_once

    @patch("panoptes_aggregation.batch_aggregation.Project")
    def test_check_permission_success(self, mock_project):
        mock_user = MagicMock()
        # Panoptes responses return strings
        mock_user.id = '100'
        mock_project.find().collaborators.return_value = [mock_user]

        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.check_permission()
        mock_project.find.assert_called_with(1)
        mock_project.find().collaborators.assert_called()
        self.assertEqual(ba.check_permission(), True)

    @patch("panoptes_aggregation.batch_aggregation.Project")
    def test_check_permission_failure(self, mock_project):
        mock_user = MagicMock()

        # List of collaborators does not include initiating user
        mock_user.id = '999'
        mock_project.find().collaborators.return_value = [mock_user]

        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.update_panoptes = MagicMock()
        ba.check_permission()
        mock_project.find.assert_called_with(1)
        mock_project.find().collaborators.assert_called()
        self.assertEqual(ba.check_permission(), False)
        ba.update_panoptes.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_run_success(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        mock_get.return_value = ({'aggregations': [{'id': 5555}]}, 'thisisanetag')
        body = {'uuid': ba.id, 'status': 'completed'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_called_with('/aggregations/5555', etag='thisisanetag', json={'aggregations': body})

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_run_failure(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        mock_get.return_value = ({'aggregations': [{'id': 5555}]}, 'thisisanetag')
        body = {'status': 'failure'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_called_with('/aggregations/5555', etag='thisisanetag', json={'aggregations': body})

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_get_failure(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        mock_get.return_value = ({'aggregations': []}, 'etag')
        body = {'status': 'failure'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.BlobServiceClient")
    def test_connect_blob_storage(self, mock_client):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.connect_blob_storage()
        ba.blob_service_client.create_container.assert_called_once_with(name=ba.id, public_access='container')
