FROM python:3.6

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN pip install --upgrade pip

# this line is still needed until hdbscan pushes to pip next
RUN pip install cython numpy

# install dependencies
COPY setup.py .
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./make_docs.sh

CMD python routes.py
