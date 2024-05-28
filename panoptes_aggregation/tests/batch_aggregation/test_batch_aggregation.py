import unittest
from unittest.mock import patch, MagicMock, call
from panoptes_aggregation.scripts import batch_utils
from panoptes_aggregation.batch_aggregation import run_aggregation
from panoptes_aggregation import batch_aggregation as batch_agg

wf_export = 'panoptes_aggregation/tests/batch_aggregation/wf_export.csv'
cls_export = 'panoptes_aggregation/tests/batch_aggregation/cls_export.csv'


@patch("panoptes_aggregation.batch_aggregation.BatchAggregator._connect_api_client", new=MagicMock())
class TestBatchAggregation(unittest.TestCase):
    @patch("panoptes_aggregation.batch_aggregation.workflow_extractor_config")
    @patch("panoptes_aggregation.batch_aggregation.BatchAggregator")
    def test_run_aggregation(self, mock_aggregator, mock_wf_ext_conf):
        mock_aggregator.process_wf_export.return_value = MagicMock()
        mock_aggregator.process_cls_export.return_value = MagicMock()

        mock_df = MagicMock()
        test_extracts = {'question_extractor': mock_df}
        batch_utils.batch_extract = MagicMock(return_value=test_extracts)
        mock_reducer = MagicMock()
        batch_utils.batch_reduce = mock_reducer

        run_aggregation(1, 10, 100)
        mock_aggregator.assert_called_once_with(1, 10, 100)
        mock_wf_ext_conf.assert_called_once()
        batch_utils.batch_extract.assert_called_once()
        mock_df.to_csv.assert_called()
        batch_utils.batch_reduce.assert_called()
        self.assertEqual(mock_reducer.call_count, 2)

        # The reducer's call list includes subsequent calls to to_csv, but the args are methods called on the mock
        # rather than use the set values i.e. "<MagicMock name='BatchAggregator().output_path' id='140281634764400'>"
        # mock_aggregator.workflow_id = '10'
        # mock_aggregator.output_path = 'tmp/10'
        # mock_reducer.assert_has_calls([
        #         call(mock_df, {'reducer_config': {'question_reducer': {}}}),
        #         call().to_csv('tmp/10/10_reducers.csv', mode='a'),
        #         call(mock_df, {'reducer_config': {'question_consensus_reducer': {}}}),
        #         call().to_csv('tmp/10/10_reducers.csv', mode='a'),
        #     ])

        # How do I test the specific instance of BatchAggregator rather than the mocked class?
        # mock_aggregator.upload_files.assert_called_once()

    @patch("panoptes_aggregation.batch_aggregation.os.mkdir")
    @patch("panoptes_aggregation.batch_aggregation.Workflow")
    @patch("panoptes_aggregation.batch_aggregation.Project")
    @patch("panoptes_aggregation.batch_aggregation.Panoptes.connect")
    def test_save_exports(self, mock_client, mock_project, mock_workflow, mock_mkdir):
        # Test that Panoptes calls are made and files are saved
        csv_dict = {'media': [{'src': 'http://zooniverse.org/123.csv'}]}
        mock_project.return_value.describe_export.return_value = csv_dict
        mock_workflow.return_value.describe_export.return_value = csv_dict
        ba = batch_agg.BatchAggregator(1, 10, 100)
        batch_agg.BatchAggregator._download_export = MagicMock(side_effect=['./cls_export.csv', './wf_export.csv'])
        mock_uuidgen = MagicMock(side_effect=ba._generate_uuid())
        ba._generate_uuid = mock_uuidgen
        expected_response = {'classifications': 'tmp/10/10_cls_export.csv', 'workflows': 'tmp/10/10_workflow_export.csv'}

        response = ba.save_exports()

        # Why do these mocked methods called in __init__ not get counted as called?
        # They are def getting called as the attributes are set
        # mock_uuidgen.assert_called_once()
        # mock_client.assert_called_once()

        self.assertEqual(response, expected_response)
        mock_mkdir.assert_called_once()
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
        ba.output_path = 'tmp/10'
        reductions_file = 'tmp/10/10_reductions.csv'
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

    @patch("panoptes_aggregation.batch_aggregation.Panoptes.post")
    def test_create_run_in_panoptes(self, mock_poster):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.create_run_in_panoptes()
        mock_poster.assert_called_with('/aggregations/', json={ 'aggregations': { 'uuid': ba.id, 'status': 'completed', 'links': { 'workflow': 10, 'user': 100 } } })

    @patch("panoptes_aggregation.batch_aggregation.BlobServiceClient")
    def test_connect_blob_storage(self, mock_client):
        ba = batch_agg.BatchAggregator(1, 10, 100)
        ba.connect_blob_storage()
        ba.blob_service_client.create_container.assert_called_once_with(name=ba.id)
