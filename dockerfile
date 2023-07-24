FROM python:3.10-slim

COPY . /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install  --without dev
#deprecated --no-dev
