FROM python:3.6-slim-stretch

RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python-dev \
    libpq-dev \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
#RUN export POETRY_VERSION=1.0.0a0
#RUN POETRY_PREVIEW=1 curl -sSL https://raw.githubusercontent.com/sdispater/poetry/develop/get-poetry.py | python
#RUN source $HOME/.poetry/env
RUN pip install 'poetry==1.0.0a0'
#RUN /bin/bash -c "source $HOME/.poetry/env"

WORKDIR ./
COPY pyproject.toml /
RUN poetry export -f requirements.txt
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY ./ ./


EXPOSE 5000

CMD ["poetry", "run", "python", "src/app.py"]
#CMD ["python", "src/app.py"]

