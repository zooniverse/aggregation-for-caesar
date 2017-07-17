FROM amazonlinux:2017.03

ENV LANG=en_US.UTF-8

# install python3.6
RUN yum update -y \
          && yum install -y \
           wget \
           gcc \
           gcc-c++ \
           openssl \
           openssl-devel \
           zlib-devel \
          && cd /usr/src \
          && wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz \
          && tar xzf Python-3.6.1.tgz \
          && cd Python-3.6.1 \
          && ./configure \
          && sed -i '205 {s/^#//}' Modules/Setup.dist \
          && sed -i '210,212 {s/^#//}' Modules/Setup.dist \
          && make \
          && make install

# install dependencies for numpy and scipy
RUN yum install -y \
                atlas-devel \
                atlas-sse3-devel \
                blas-devel \
                git \
                lapack-devel \
                findutils \
                zip

# make venv
RUN python3 -m venv --system-site-packages /usr/src/env/zappa_env \
          && echo '. /usr/src/env/zappa_env/bin/activate' >> /root/.bashrc

# compile numpy and scipy
RUN . /usr/src/env/zappa_env/bin/activate \
          && pip3 install --upgrade pip wheel \
          && pip3 install --use-wheel --no-binary numpy numpy \
          && pip3 install --use-wheel --no-binary scipy scipy

# compile latest version of sklearn that fixes "_bz2" import issues
RUN . /usr/src/env/zappa_env/bin/activate \
          && cd /usr/src \
          && git clone https://github.com/scikit-learn/scikit-learn.git \
          && cd scikit-learn \
          && pip3 install cython \
          && pip3 install --use-wheel . \
          && pip3 uninstall -y cython

WORKDIR /usr/src/aggregation

# move shared libs
RUN . /usr/src/env/zappa_env/bin/activate \
          && libdir="/usr/src/env/zappa_env/lib64/python3.6/site-packages/lib/" \
          && mkdir /usr/src/env/zappa_env/lib64/python3.6/site-packages/lib \
          && cp /usr/lib64/atlas/* $libdir \
          && cp /usr/lib64/libquadmath.so.0 $libdir \
          && cp /usr/lib64/libgfortran.so.3 $libdir

# install other requirements
COPY requirements.txt ./
RUN . /usr/src/env/zappa_env/bin/activate \
          && pip3 install -r requirements.txt

# reduce the size of all packages
RUN find /usr/src/env/zappa_env/lib64/python3.6/site-packages/ -name "*.so" | xargs strip \
          && find /usr/src/env/zappa_env/lib64/python3.6/site-packages/scipy/ -type d -name 'tests' -exec rm -r {} + \
          && find /usr/src/env/zappa_env/lib64/python3.6/site-packages/sklearn/ -type d -name 'tests' -exec rm -r {} + \
          && find /usr/src/env/zappa_env/lib64/python3.6/site-packages/numpy/ -type d -name 'tests' -exec rm -r {} +

COPY . ./

CMD . /usr/src/env/zappa_env/bin/activate \
            && python3 routs.py
