FROM python:3

ENV LANG=en_US.UTF-8

WORKDIR /usr/src/aggregation

# install other requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD python routs.py
