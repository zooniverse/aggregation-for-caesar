FROM python:3.7-slim

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN apt-get update && apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY setup.py .
RUN pip install --upgrade pip
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./make_docs.sh

# load configs and start flask app
CMD ["bash", "./start-flask.sh"]
