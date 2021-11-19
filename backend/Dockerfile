FROM python:3.7-alpine
MAINTAINER Joao Gabriel Coli

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --no-cache 	mariadb-dev postgresql-dev && \
    apk add --no-cache --virtual .build-deps gcc g++ make musl-dev libressl-dev libffi-dev mariadb-dev postgresql-dev
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN adduser -D jcoli
RUN chown jcoli:jcoli -R /app/
USER jcoli