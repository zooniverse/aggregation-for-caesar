#!/bin/bash -e

# load configs if present
if [ "$FLASK_ENV" != "development" ]; then
  if [ -f /run/secrets/environment ]
  then
      source /run/secrets/environment
  fi
fi

exec python panoptes_aggregation/routes.py