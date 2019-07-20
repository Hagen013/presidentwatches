FROM alpine:latest

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    build-base \
    libffi-dev \
    linux-headers \
    && pip3 install --upgrade pip \
    && pip3 install numpy \
    && pip3 install pandas \
    && pip3 install --no-cache-dir psycopg2

# INSTALL UWSGI
RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket

# INSTALL PILLOW 
RUN apk add --no-cache \
    py3-pillow

# INSTALL BASH
RUN apk add --update --no-cache bash


# INSTALL REQUIREMENTS
COPY  server/requirements/base.txt base.txt
COPY  server/requirements/production.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# COPY ENTRYPOINT AND CODE
COPY  server /server
COPY  client /client
COPY  compose/celery_pw/uwsgi.ini uwsgi.ini
COPY  compose/celery_pw/entrypoint.sh entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/entrypoint.sh"]