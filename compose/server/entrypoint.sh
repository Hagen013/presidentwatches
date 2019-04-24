#!/bin/bash
set -e
cmd="$@"

function postgres_ready(){
python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname='$DJANGO_POSTGRES_DATABASE', user='$DJANGO_POSTGRES_USER', password='$DJANGO_POSTGRES_PASSWORD', host='$DJANGO_POSTGRES_HOST')
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

function elasticsearch_ready(){
python3 << END
import time
import json
import sys

import requests

ELASTICSEARCH_URL = 'http://elasticsearch:9200/'
SNAPSHOT_REPO = 'backups'
SNAPSHOT_NAME = 'backup'

index = 'store'
doc_type = 'product'

health_url = ELASTICSEARCH_URL + '_cat/health'

try:
    response = requests.get(url=health_url)
    status_code = response.status_code
    if status_code == 200:

        restore_url = ELASTICSEARCH_URL + '{repo}/{name}'.format(repo=SNAPSHOT_REPO, name=SNAPSHOT_NAME)
        requests.post(restore_url)

        sys.exit(0)
    else:
        print('Elasticsearch invalid status code: {0}'.format(
            status_code
        ))
        sys.exit(-1)
except requests.exceptions.RequestException:
    sys.exit(-1)
END
}


until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing..."

until elasticsearch_ready; do
  >&2 echo "Elasticsearch is unavailable - sleeping"
  sleep 1
done
>&2 echo "Elasticsearch is up - continuing..."


python3 /server/manage.py migrate && \
        uwsgi --plugin python3 --ini ./uwsgi.ini

exec $cmd
