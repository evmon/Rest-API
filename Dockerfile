FROM python:3.6.5-alpine3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /srv/app

COPY requirements.txt /srv/app
COPY requirements-dev.txt /srv/app

RUN apk update && apk add --no-cache \
    gcc \
    make \
    libc-dev \
    musl-dev \
    linux-headers \
    pcre-dev \
    postgresql-dev \
    postgresql-client \
    redis

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY app /srv/app

COPY docker/start.sh /usr/local/bin/docker-app-start

CMD ["docker-app-start"]
