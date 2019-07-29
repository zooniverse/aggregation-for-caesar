FROM python:3.7

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN pip install --upgrade pip

# install dependencies
COPY setup.py .
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./make_docs.sh

# load configs and start flask app
CMD ["bash", "./start-flask.sh"]
