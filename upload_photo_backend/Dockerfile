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


#COPY ./compose/local/django/entrypoint /entrypoint
#RUN sed -i 's/\r$//g' /entrypoint
#RUN chmod +x /entrypoint
#
#COPY ./compose/local/django/start /start
#RUN sed -i 's/\r$//g' /start
#RUN chmod +x /start

COPY ./compose/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' start-celeryworker
RUN chmod +x start-celeryworker

COPY ./compose/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' start-celerybeat
RUN chmod +x start-celerybeat

COPY ./compose/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' start-flower
RUN chmod +x start-flower


#ENTRYPOINT ["/entrypoint"]
