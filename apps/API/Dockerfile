FROM ubuntu:18.04
FROM python:3.8

RUN apt-get update

# Install system dependencies with OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        libopencv-dev \ 
        build-essential \
        libssl-dev \
        libpq-dev \
        libcurl4-gnutls-dev \
        libexpat1-dev \
        python3-setuptools \
        python3-pip \
        python3-dev \
        protobuf-compiler \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip 

RUN mkdir /app
WORKDIR /app

# COPY requirements_api.txt .
# RUN pip install --no-cache-dir -r requirements_api.txt

COPY requirements_model_new.txt .
RUN pip install --no-cache-dir -r requirements_model_new.txt

# COPY run.py .

RUN mkdir /app/api
WORKDIR /app/api
COPY /api/ .

WORKDIR /app/api/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
RUN python -m pip install .

WORKDIR /app

# EXPOSE 8000
# ENV FLASK_APP=run.py
# CMD ["flask", "run", "--host", "0.0.0.0","--port","8000"]

CMD gunicorn api.wsgi:app --bind 0.0.0.0:$PORT

## DEBUGGING
## sudo docker run -it --entrypoint /bin/bash <ImageID>