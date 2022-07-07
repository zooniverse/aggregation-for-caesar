FROM python:3.10-slim as builder

ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PDM_USE_VENV=True

WORKDIR /usr/src/aggregation
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
    build-essential libgeos-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY pyproject.toml pdm.lock README.md ./
RUN pip install --upgrade pip && \
    pip install --pre pdm && \
    pdm sync --no-editable --no-isolation --no-self -G online -G test -G doc

# activate venv
ENV VIRTUAL_ENV=/usr/src/aggregation/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install package
COPY . .
RUN pdm sync --no-isolation -G online -G test -G doc

# make documentation
RUN ./make_docs.sh

FROM python:3.10-slim as runner
WORKDIR /usr/src/aggregation

# copy code, venv, and docs from builder stage
COPY --from=builder /usr/src/aggregation/ /usr/src/aggregation/

SHELL ["/bin/bash", "-c"]

# activate venv
ENV VIRTUAL_ENV=/usr/src/aggregation/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG REVISION=''
ENV REVISION=$REVISION

# load configs and start flask app
CMD ./start-flask.sh
