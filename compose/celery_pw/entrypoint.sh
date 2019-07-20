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

function redis_ready(){
python3 << END
import redis
import sys
rs = redis.Redis('redis')
try:
    response = rs.client_list()
except redis.ConnectionError:
    sys.exit(-1)
sys.exit(0)
END
}

function rabbit_ready(){
python3 << END
from kombu import Connection
import sys
rabbit_url = 'amqp://$RABBIT_USER:$RABBIT_PASS@$RABBIT_HOSTNAME/$RABBIT_VHOST'
conn = Connection(rabbit_url)
try:
    conn.connect()
except:
    sys.exit(-1)
sys.exit(0)
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

until redis_ready; do
  >&2 echo "Redis is unavailable - sleeping"
  sleep 1
done
>&2 echo "Redis is up - continuing..."

until rabbit_ready; do
  >&2 echo "Rabbit is unavailable - sleeping"
  sleep 1
done
>&2 echo "Rabbit is up - continuing..."

>&2 cd server

>&2 celery -A config worker -l info -E -Q default -n default_worker.%h --concurrency=2 -B

exec $cmd
