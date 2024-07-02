#!/bin/bash -e

# if there is no endpoints file create it
if ! [ -f endpoints.yml ]; then
  cp endpoints.yml.template endpoints.yml
fi

LISTEN_PORT=${LISTEN_PORT:=80}
exec newrelic-admin run-program gunicorn -b 0.0.0.0:$LISTEN_PORT -w 4 -t 120 "panoptes_aggregation.routes:make_application()"
