FROM python:3.9-slim
ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN apt-get update && apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
    build-essential libgeos-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN mkdir -p panoptes_aggregation/version
COPY pyproject.toml README.md ./
COPY panoptes_aggregation/__init__.py ./panoptes_aggregation/
COPY panoptes_aggregation/version/__init__.py ./panoptes_aggregation/version/
RUN pip install --upgrade pip
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./make_docs.sh

ARG REVISION=''
ENV REVISION=$REVISION

# load configs and start flask app
CMD ["bash", "./start-flask.sh"]
