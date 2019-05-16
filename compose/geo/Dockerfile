FROM graphmarket/base_alpine:latest

# INSTALL UWSGI
RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# INSTALL REQUIREMENTS
COPY  geo/requirements/base.txt base.txt
COPY  geo/requirements/production.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# INSTALL BASH
RUN apk add --update --no-cache bash

# COPY ENTRYPOINT AND CODE
COPY  geo /geo
COPY  compose/geo/uwsgi.ini uwsgi.ini
COPY  compose/geo/entrypoint.sh entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8002
EXPOSE 8282

ENTRYPOINT ["/entrypoint.sh"]
