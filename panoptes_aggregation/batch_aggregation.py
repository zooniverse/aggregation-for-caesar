from celery import Celery
import json
import pandas as pd
import os
import sys
import urllib3
from shutil import make_archive
import uuid

from azure.storage.blob import BlobServiceClient

from panoptes_client import Panoptes, Project, Workflow
from panoptes_aggregation.workflow_config import workflow_extractor_config
from panoptes_aggregation.scripts import batch_utils

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="run_aggregation")
def run_aggregation(project_id, workflow_id, user_id):
    ba = BatchAggregator(project_id, workflow_id, user_id)

    if not ba.check_permission():
        print(f'[Batch Aggregation] Unauthorized attempt by user {user_id} to aggregate workflow {workflow_id}')
        # Exit the task gracefully without retrying or erroring
        sys.exit()

    print(f'[Batch Aggregation] Run beginning for workflow {workflow_id} by user {user_id}')

    print(f'[Batch Aggregation] Saving exports for workflow {workflow_id})')
    ba.save_exports()

    print(f'[Batch Aggregation] Processing exports for workflow {workflow_id})')
    ba.process_wf_export(ba.wf_csv)
    cls_df = ba.process_cls_export(ba.cls_csv)

    print(f'[Batch Aggregation] Extacting workflow {workflow_id})')
    extractor_config = workflow_extractor_config(ba.tasks)
    extracted_data = batch_utils.batch_extract(cls_df, extractor_config, hide_progressbar=True)

    batch_standard_reducers = {
        'question_extractor': ['question_reducer', 'question_consensus_reducer'],
        'survey_extractor': ['survey_reducer']
    }

    print(f'[Batch Aggregation] Reducing workflow {workflow_id})')
    for task_type, extract_df in extracted_data.items():
        csv_filepath = os.path.join(ba.output_path, f'{ba.workflow_id}_{task_type}.csv')
        extract_df.to_csv(csv_filepath)
        reducer_list = batch_standard_reducers[task_type]
        reduced_data = {}

        for reducer in reducer_list:
            # This is an override. The workflow_reducer_config method returns a config object
            # that is incompatible with the batch_utils batch_reduce method
            reducer_config = {'reducer_config': {reducer: {}}}
            reduced_data[reducer] = batch_utils.batch_reduce(extract_df, reducer_config, hide_progressbar=True)
            # filename = f'{ba.output_path}/{ba.workflow_id}_reductions.csv'
            filename = os.path.join(ba.output_path, f'{ba.workflow_id}_reductions.csv')
            reduced_data[reducer].to_csv(filename, mode='a')

    # Upload zip & reduction files to blob storage
    print(f'[Batch Aggregation] Uploading results for {workflow_id})')
    ba.upload_files()

    # This could catch PanoptesAPIException, but what to do if it fails?
    print(f'[Batch Aggregation] Updating Panoptes for {workflow_id})')
    success_attrs = {'uuid': ba.id, 'status': 'completed'}
    ba.update_panoptes(success_attrs)

    # STDOUT messages get printed to kubernetes logs
    print(f'[Batch Aggregation] Run successful for workflow {workflow_id} by user {user_id}')


class BatchAggregator:
    """
    Bunch of stuff to manage a batch aggregation run
    """

    def __init__(self, project_id, workflow_id, user_id):
        self.project_id = int(project_id)
        self.workflow_id = int(workflow_id)
        self.user_id = int(user_id)
        self._generate_uuid()
        self._connect_api_client()

    def save_exports(self):
        self.output_path = os.path.join('tmp', str(self.id))
        os.makedirs(self.output_path)

        cls_export = Workflow(self.workflow_id).describe_export('classifications')
        full_cls_url = cls_export['media'][0]['src']
        cls_file = os.path.join(self.output_path, f'{self.workflow_id}_cls_export.csv')

        self._download_export(full_cls_url, cls_file)

        wf_export = Project(self.project_id).describe_export('workflows')
        full_wf_url = wf_export['media'][0]['src']
        wf_file = os.path.join(self.output_path, f'{self.workflow_id}_workflow_export.csv')
        self._download_export(full_wf_url, wf_file)

        self.cls_csv = cls_file
        self.wf_csv = wf_file
        return {'classifications': cls_file, 'workflows': wf_file}

    def process_wf_export(self, wf_csv):
        self.wf_df = pd.read_csv(wf_csv)
        self.wf_maj_version = self.wf_df.query(f'workflow_id == {self.workflow_id}')['version'].max()
        self.wf_min_version = self.wf_df.query(f'workflow_id == {self.workflow_id} & version == {self.wf_maj_version}')['minor_version'].max()
        self.workflow_version = f'{self.wf_maj_version}.{self.wf_min_version}'
        self.workflow_row = self.wf_df.query(f'workflow_id == {self.workflow_id} & minor_version == {self.wf_min_version}')
        self.tasks = json.loads(self.workflow_row.iloc[0]['tasks'])
        return self.wf_df

    def process_cls_export(self, cls_csv):
        cls_df = pd.read_csv(cls_csv)
        self.cls_df = cls_df.query(f'workflow_version == {self.workflow_version}')
        return self.cls_df

    def connect_blob_storage(self):
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        self.blob_service_client.create_container(name=self.id, public_access='container')

    def upload_file_to_storage(self, container_name, filepath):
        blob = filepath.split('/')[-1]
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob)
        with open(file=filepath, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def upload_files(self):
        self.connect_blob_storage()
        reductions_file = os.path.join(self.output_path, f'{self.workflow_id}_reductions.csv')
        self.upload_file_to_storage(self.id, reductions_file)
        zippath = os.path.join('tmp', self.id)
        zipfile = make_archive(zippath, 'zip', self.output_path)
        self.upload_file_to_storage(self.id, zipfile)

    def update_panoptes(self, body_attributes):
        # An Aggregation class can be added to the python client to avoid doing this manually
        params = {'workflow_id': self.workflow_id}
        response = Panoptes.client().get('/aggregations', params=params)
        if not response[0]['aggregations']:
            print('[Batch Aggregation] Panoptes Aggregation resource not found. Unable to update.')
            return False
        agg_id = response[0]['aggregations'][0]['id']
        fresh_etag = response[1]

        Panoptes.client().put(
            f'/aggregations/{agg_id}',
            etag=fresh_etag,
            json={'aggregations': body_attributes}
        )

    def check_permission(self):
        project = Project.find(self.project_id)
        permission = False
        for user in project.collaborators():
            if user.id == str(self.user_id):
                permission = True
        return permission

    def _generate_uuid(self):
        self.id = uuid.uuid4().hex

    def _download_export(self, url, filepath):
        http = urllib3.PoolManager()
        r = http.request('GET', url, preload_content=False)
        with open(filepath, 'wb') as out:
            while True:
                data = r.read(65536)
                if not data:
                    break
                out.write(data)
        r.release_conn()

    def _connect_api_client(self):
        # connect to the API only once for this function request
        Panoptes.connect(
            endpoint=os.getenv('PANOPTES_URL', 'https://panoptes.zooniverse.org/'),
            client_id=os.getenv('PANOPTES_CLIENT_ID'),
            client_secret=os.getenv('PANOPTES_CLIENT_SECRET'),
            admin='true'
        )
