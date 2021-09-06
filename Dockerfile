FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc python3-dev musl-dev linux-headers postgresql-dev
RUN apk add --no-cache jpeg-dev zlib-dev libjpeg libpq

RUN pip install -r requirements.txt

RUN apk del .tmp

COPY . /app