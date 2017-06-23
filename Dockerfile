FROM python:3.6.1

WORKDIR /usr/src/aggregation

COPY requirements.txt ./

RUN python3 -m venv --system-site-packages /usr/src/env/zappa
RUN echo '. /usr/src/env/zappa/bin/activate' >> /root/.bashrc
RUN . /usr/src/env/zappa/bin/activate \
          && pip install -r requirements.txt
RUN . /usr/src/env/zappa/bin/activate \
          && pip install -U scikit-learn

COPY . ./

CMD . /usr/src/env/zappa/bin/activate \
            && python routs.py
