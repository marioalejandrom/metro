FROM python:3.7-alpine
MAINTAINER Mario Morales

ENV PYTHONUNBUFFERED 1

# Dependencies
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-dependencies \
    gcc libc-dev linux-headers postgresql-dev \
    musl-dev openssl-dev libffi-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-dependencies

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user