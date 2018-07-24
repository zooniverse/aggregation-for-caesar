FROM python:3.7

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

# install requirements
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN cat requirements.txt | xargs -n 1 -L 1 pip install --no-cache-dir

COPY . ./

# make documentation
RUN /bin/bash -lc ./make_docs.sh

CMD python routes.py
