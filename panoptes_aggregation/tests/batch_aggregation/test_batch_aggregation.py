try:
    from panoptes_aggregation.scripts import batch_utils
    from panoptes_aggregation.batch_aggregation import run_aggregation
    from panoptes_aggregation import batch_aggregation as batch_agg
    import jwt

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
            run_aggregation(1, 10, 'fake-token')
        mock_aggregator_instance.update_panoptes.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.pd.concat")
    @patch("panoptes_aggregation.batch_aggregation.workflow_extractor_config")
    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator")
    def test_run_aggregation_success(self, mock_aggregator, mock_wf_ext_conf, mock_concat):
        mock_aggregator_instance = mock_aggregator.return_value
        mock_aggregator_instance.check_permission.return_value = True

        mock_df = MagicMock()
        test_extracts = {'question_extractor': mock_df}
        batch_utils.batch_extract = MagicMock(return_value=test_extracts)
        mock_reducer = MagicMock()
        batch_utils.batch_reduce = mock_reducer
        mock_combo_df = MagicMock()
        mock_concat.return_value = mock_combo_df

        run_aggregation(1, 10, 'fake-token')
        mock_aggregator_instance.check_permission.assert_called_once()
        mock_aggregator.assert_called_once_with(1, 10, 'fake-token')
        mock_wf_ext_conf.assert_called_once()
        batch_utils.batch_extract.assert_called_once()
        mock_df.to_csv.assert_called()
        batch_utils.batch_reduce.assert_called()
        self.assertEqual(mock_reducer.call_count, 2)
        mock_combo_df.to_csv.assert_called_once()
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

    @patch("panoptes_aggregation.batch_aggregation.Workflow")
    @patch("panoptes_aggregation.batch_aggregation.os.makedirs")
    def test_save_exports_panoptes_exception(self, mock_makedirs, mock_workflow):
        from panoptes_aggregation.batch_aggregation import PanoptesAPIException

        error_string = 'No classifications_export exists for workflow #10'
        mock_workflow.return_value.describe_export.side_effect = PanoptesAPIException(error_string)
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.id = 'asdf123asdf'
        ba.update_panoptes = MagicMock()

        # Patch sys.exit to prevent the test from exiting
        with patch("sys.exit", side_effect=SystemExit):
            with self.assertRaises(SystemExit):
                ba.save_exports()

        ba.update_panoptes.assert_called_once_with({'uuid': ba.id, 'status': 'failed', 'error': error_string})
        mock_makedirs.assert_not_called()
        mock_workflow.assert_called_once_with(10)
        mock_workflow.return_value.describe_export.assert_called_once_with('classifications')

    def test_process_wf_export(self):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        result = ba.process_wf_export(wf_export)
        self.assertEqual(ba.wf_maj_version, 16)
        self.assertEqual(ba.wf_min_version, 55)
        self.assertEqual(ba.workflow_version, '16.55')
        self.assertEqual(result.__class__.__name__, 'DataFrame')

    def test_process_cls_export(self):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        ba.workflow_version = '16.55'
        result = ba.process_cls_export(cls_export)
        self.assertEqual(result.__class__.__name__, 'DataFrame')

    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator.connect_blob_storage")
    @patch("panoptes_aggregation.batch_aggregation.make_archive")
    def test_upload_files(self, archive_mock, client_mock):
        zipped_mock = MagicMock()
        archive_mock.return_value = zipped_mock
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        ba.upload_file_to_storage = MagicMock()
        ba.output_path = os.path.join('tmp', '10')
        reductions_file = os.path.join('tmp', '10', '10_reductions.csv')
        ba.upload_files()
        client_mock.assert_called_once()
        archive_mock.assert_called_once()
        ba.upload_file_to_storage.assert_has_calls([call(ba.id, reductions_file), call(ba.id, zipped_mock)])

    def test_upload_file_to_storage(self):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        mock_client = MagicMock()
        ba.blob_service_client = MagicMock(return_value=mock_client)
        ba.upload_file_to_storage('asdf123asdf', cls_export)
        mock_client.upload_blob.assert_called_once

    @patch("panoptes_aggregation.batch_aggregation.Project")
    @patch("builtins.open")
    @patch("panoptes_aggregation.batch_aggregation.os.path.exists")
    def test_check_permission_success_admin(self, mock_exists, mock_open, mock_project):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = "test-public-key"
        mock_open.return_value.__enter__.return_value = mock_file

        ba = batch_agg.BatchAggregator(1, 10, "fake-token")
        ba.decoded_token = {'data': {'id': 100, 'admin': True}}
        ba.is_admin = True
        ba.user_id = 100

        # Admin should have permission regardless of collaborator status
        self.assertTrue(ba.check_permission())
        # Project lookup not needed for admin
        mock_project.find.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.Project")
    @patch("builtins.open")
    @patch("panoptes_aggregation.batch_aggregation.os.path.exists")
    def test_check_permission_success_collaborator(self, mock_exists, mock_open, mock_project):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = "test-public-key"
        mock_open.return_value.__enter__.return_value = mock_file

        ba = batch_agg.BatchAggregator(1, 10, "fake-token")
        ba.decoded_token = {'data': {'id': 100, 'admin': False}}
        ba.is_admin = False
        ba.user_id = 100

        mock_user = MagicMock()
        mock_user.id = '100'
        mock_project.find().collaborators.return_value = [mock_user]

        self.assertTrue(ba.check_permission())
        mock_project.find.assert_called_with(1)
        mock_project.find().collaborators.assert_called()

    @patch("panoptes_aggregation.batch_aggregation.Project")
    @patch("builtins.open")
    @patch("panoptes_aggregation.batch_aggregation.os.path.exists")
    def test_check_permission_failure(self, mock_exists, mock_open, mock_project):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = "test-public-key"
        mock_open.return_value.__enter__.return_value = mock_file

        ba = batch_agg.BatchAggregator(1, 10, "fake-token")
        ba.decoded_token = {'data': {'id': 100, 'admin': False}}
        ba.is_admin = False
        ba.user_id = 100
        ba.update_panoptes = MagicMock()

        diff_user = MagicMock()
        diff_user.id = '999'
        mock_project.find().collaborators.return_value = [diff_user]

        self.assertFalse(ba.check_permission())
        mock_project.find.assert_called_with(1)
        mock_project.find().collaborators.assert_called()
        ba.update_panoptes.assert_not_called()

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_run_success(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        mock_get.return_value = ({'aggregations': [{'id': 5555}]}, 'thisisanetag')
        body = {'uuid': ba.id, 'status': 'completed'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_called_with('/aggregations/5555', etag='thisisanetag', json={'aggregations': body})

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_run_failure(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        mock_get.return_value = ({'aggregations': [{'id': 5555}]}, 'thisisanetag')
        body = {'status': 'failure'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_called_with('/aggregations/5555', etag='thisisanetag', json={'aggregations': body})

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.put")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.get")
    def test_update_panoptes_get_failure(self, mock_get, mock_put):
        ba = batch_agg.BatchAggregator(1, 10, 'fake-token')
        mock_get.return_value = ({'aggregations': []}, 'etag')
        body = {'status': 'failure'}
        ba.update_panoptes(body)
        mock_get.assert_called_with('/aggregations', params={'workflow_id': 10})
        mock_put.assert_not_called()

    @patch('panoptes_aggregation.batch_aggregation.os.path.exists')
    @patch('builtins.open')
    @patch('jwt.decode')
    def test_jwt_token_verification_success(self, mock_decode, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = "test-public-key"
        mock_open.return_value.__enter__.return_value = mock_file

        token_payload = {
            'data': {
                'id': 123,
                'admin': True
            }
        }
        mock_decode.return_value = token_payload
        jwt_token = "fake-token"

        ba = batch_agg.BatchAggregator(1, 10, jwt_token)

        self.assertEqual(ba.user_id, 123)
        self.assertTrue(ba.is_admin)
        self.assertEqual(ba.decoded_token, token_payload)
        mock_decode.assert_called_once_with(jwt_token, "test-public-key", algorithms=['RS512'])

    @patch('panoptes_aggregation.batch_aggregation.os.path.exists')
    def test_jwt_token_verification_missing_key_file(self, mock_exists):
        mock_exists.return_value = False
        ba = batch_agg.BatchAggregator(1, 10, "invalid-token")

        self.assertIsNone(ba.decoded_token)
        self.assertIsNone(ba.user_id)
        self.assertFalse(ba.is_admin)

    @patch('panoptes_aggregation.batch_aggregation.os.path.exists')
    @patch('builtins.open')
    @patch('jwt.decode')
    def test_jwt_token_verification_invalid_token(self, mock_jwt_decode, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_file = MagicMock(read=MagicMock(return_value="test-public-key"))
        mock_open.return_value = mock_file
        mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")

        ba = batch_agg.BatchAggregator(1, 10, "invalid-token")

        self.assertIsNone(ba.decoded_token)
        self.assertIsNone(ba.user_id)
        self.assertFalse(ba.is_admin)

    @patch('panoptes_aggregation.batch_aggregation.os.path.exists')
    @patch('builtins.open')
    @patch('jwt.decode')
    def test_jwt_token_admin_permission(self, mock_jwt_decode, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_file = MagicMock(read=MagicMock(return_value="test-public-key"))
        mock_open.return_value = mock_file

        admin_payload = {
            'data': {
                'id': 123,
                'admin': True
            }
        }
        mock_jwt_decode.return_value = admin_payload

        ba = batch_agg.BatchAggregator(1, 10, "admin-token")
        self.assertTrue(ba.check_permission())

    @patch('panoptes_aggregation.batch_aggregation.os.path.exists')
    @patch('builtins.open')
    @patch('jwt.decode')
    @patch('panoptes_aggregation.batch_aggregation.Project')
    def test_jwt_token_non_admin_permission(self, mock_project, mock_jwt_decode, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_file = MagicMock(read=MagicMock(return_value="test-public-key"))
        mock_open.return_value = mock_file

        non_admin_payload = {
            'data': {
                'id': 123,
                'admin': False
            }
        }
        mock_jwt_decode.return_value = non_admin_payload
        mock_project.find().collaborators.return_value = []

        ba = batch_agg.BatchAggregator(1, 10, "non-admin-token")
        self.assertFalse(ba.check_permission())
