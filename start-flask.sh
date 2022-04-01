#!/bin/bash -e

# set REVISION env var from commit_id.txt or default
export COMMIT_ID=$(cat commit_id.txt 2> /dev/null)
export REVISION="${COMMIT_ID:-asdf123jkl456}"

# if there is no endpoints file create it
if ! [ -f endpoints.yml ]; then
  cp endpoints.yml.template endpoints.yml
fi

LISTEN_PORT=${LISTEN_PORT:=80}
exec newrelic-admin run-program gunicorn -b 0.0.0.0:$LISTEN_PORT -w 4 -t 120 "panoptes_aggregation.routes:make_application()"
