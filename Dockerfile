FROM python:3

ENV LANG=en_US.UTF-8

WORKDIR /usr/src/aggregation

# install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# make documentation
RUN /bin/bash -lc ./make_docs.sh

CMD python routs.py
