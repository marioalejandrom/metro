FROM python:3.7-alpine
MAINTAINER Mario Morales

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-dependencies \
    gcc libffi-dev linux-headers musl-dev openssl-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-dependencies

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user