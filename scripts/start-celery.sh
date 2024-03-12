#!/bin/bash -e

exec celery --app panoptes_aggregation.tasks.celery worker --loglevel=info
