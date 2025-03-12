FROM python:3.13-slim
ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN apt-get update && apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
    build-essential libgeos-dev git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN mkdir -p panoptes_aggregation/version
COPY pyproject.toml README.md LICENSE ./
COPY panoptes_aggregation/__init__.py ./panoptes_aggregation/
COPY panoptes_aggregation/version/__init__.py ./panoptes_aggregation/version/
RUN pip install --upgrade pip
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./scripts/make_docs.sh

# ADD ./ /usr/src/aggregation

ARG REVISION=''
ENV REVISION=$REVISION

# load configs and start flask app
CMD ["bash", "./scripts/start-flask.sh"]
