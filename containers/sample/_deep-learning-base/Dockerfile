# Multi-stage Dockerfile for the poetry-based project
# The builder image, used to build the virtual environment
FROM python:3.10-buster as builder

RUN pip install poetry==1.6.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --no-interaction

# The runtime image, used to just run the code provided its virtual environment
FROM us-docker.pkg.dev/deeplearning-platform-release/gcr.io/tf2-cpu.2-15.py310:latest as runtime
# Deep Learning Containers
# https://cloud.google.com/deep-learning-containers/docs/choosing-container
# FROM us-docker.pkg.dev/deeplearning-platform-release/gcr.io/pytorch-gpu.1-13.py310:latest as runtime

ENV REQUIREMENTS=/app/requirements.txt

COPY --from=builder ${REQUIREMENTS} ${REQUIREMENTS}

RUN pip install -r ${REQUIREMENTS}
