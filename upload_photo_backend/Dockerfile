FROM python:3.10-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

EXPOSE 8000

RUN python -m venv /py && \
    pip install --upgrade pip && \
    # installing necessary packages to install psycopg2 from source
    # because this version is more robust/efficient than psycopg2-binary
    # added gcc, musl-dev ... - is it necessary
    apk add gcc musl-dev python3-dev libffi-dev openssl-dev && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    pip install -r requirements.txt && \
    # remove unnecessary packages used to build psycopg2
    apk del .tmp-build-deps
