#!/bin/bash -e

BROKER=${CELERY_BROKER_URL:='redis://redis:6379/0'}
exec celery --app panoptes_aggregation.tasks.celery flower --port=5555 --broker=$BROKER
