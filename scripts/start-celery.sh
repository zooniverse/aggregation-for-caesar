#!/bin/bash -e

exec celery --app panoptes_aggregation.batch_aggregation.celery worker --loglevel=info
