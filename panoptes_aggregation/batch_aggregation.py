from celery import Celery
import json
import pandas as pd
import os
import urllib3
import pandas as pd

from panoptes_client import Panoptes, Project, Workflow
from panoptes_aggregation.workflow_config import workflow_extractor_config, workflow_reducer_config
from panoptes_aggregation.scripts import batch_utils
from panoptes_client.panoptes import PanoptesAPIException

import logging
panoptes_client_logger = logging.getLogger('panoptes_client').setLevel(logging.ERROR)

from panoptes_client import Panoptes, Project, Workflow

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="run_aggregation")
def run_aggregation(project_id, workflow_id, user_id):
    ba = BatchAggregator(project_id, workflow_id, user_id)
    exports = ba.save_exports()
    wf_df = ba.process_wf_export(ba.wf_csv)
    cls_df = ba.process_cls_export(ba.cls_csv)

    extractor_config = workflow_extractor_config(ba.tasks)
    extracted_data = batch_utils.batch_extract(cls_df, extractor_config)

    reducer_config = workflow_reducer_config(extractor_config)
    reduced_data = batch_utils.batch_reduce(extracted_data, reducer_config)

class BatchAggregator:
    """
    Bunch of stuff to manage a batch aggregation run
    """

    def __init__(self, project_id, workflow_id, user_id):
        self.project_id = project_id
        self.workflow_id = workflow_id
        self.user_id = user_id
        self._connect_api_client()

    def save_exports(self):
        cls_export = Workflow(self.workflow_id).describe_export('classifications')
        full_cls_url = cls_export['media'][0]['src']
        wf_export = Project(self.project_id).describe_export('workflows')
        full_wf_url = wf_export['media'][0]['src']
        cls_file = f'tmp/{self.workflow_id}_cls_export.csv'
        self._download_export(full_cls_url, cls_file)
        wf_file = f'tmp/{self.project_id}_workflow_export.csv'
        self._download_export(full_wf_url, wf_file)
        self.cls_csv = cls_file
        self.wf_csv = wf_file
        return {'cls_csv': cls_file, 'wf_csv': wf_file}

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
        # Panoptes.connect(
            # endpoint=getenv('PANOPTES_URL', 'https://panoptes.zooniverse.org/'),
            # client_id=getenv('PANOPTES_CLIENT_ID'),
            # client_secret=getenv('PANOPTES_CLIENT_SECRET')
        # )