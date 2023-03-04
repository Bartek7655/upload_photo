FROM python:3.10-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN python -m venv /py && \
    pip install --upgrade pip && \
    # installing necessary packages to install psycopg2 from source
    # because this version is more robust/efficient than psycopg2-binary
    # added gcc, musl-dev ... - is it necessary
    apk add gcc musl-dev python3-dev libffi-dev openssl-dev && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    pip install -r app/requirements.txt && \
    # remove unnecessary packages used to build psycopg2
    apk del .tmp-build-deps &&\
    apk add bash


COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celery-worker
RUN sed -i 's/\r$//g' /start-celery-worker
RUN chmod +x /start-celery-worker

COPY ./compose/local/django/celery/beat/start /start-celery-beat
RUN sed -i 's/\r$//g' /start-celery-beat
RUN chmod +x /start-celery-beat

COPY ./compose/local/django/celery/flower/start /start-celery-flower
RUN sed -i 's/\r$//g' /start-celery-flower
RUN chmod +x /start-celery-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
