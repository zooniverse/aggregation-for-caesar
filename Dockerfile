FROM python:3.10-slim

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN apt-get update && apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
    build-essential libgeos-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY pyproject.toml pdm.lock README.md ./
COPY panoptes_aggregation/version/__init__.py ./panoptes_aggregation/version/
RUN pip install --upgrade pip
RUN pip install --pre pdm
RUN pdm config python.use_venv True
RUN pdm sync --no-editable --no-isolation --no-self -G online -G test -G doc

# install package
COPY . .
RUN pdm install -G online -G test -G doc

# activate venv
ENV VIRTUAL_ENV=/usr/src/aggregation/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# make documentation
RUN chmod +x make_docs
RUN /bin/bash -lc ./make_docs.sh

ARG REVISION=''
ENV REVISION=$REVISION

# load configs and start flask app
CMD ["bash", "./start-flask.sh"]
