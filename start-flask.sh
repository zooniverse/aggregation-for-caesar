#!/bin/bash -e

# if there is no endpoints file create it
if ! [ -f endpoints.yml ]; then
  cp endpoints.yml.template endpoints.yml
fi

exec python panoptes_aggregation/routes.py