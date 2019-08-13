import os
import json
import shutil
import datetime

from django.conf import settings

import requests
from elasticsearch_dsl.connections import connections

from config.es_client import es_client
from config.celery import app
from celery.signals import beat_init
from celery.schedules import crontab

from shop.models import ProductPage, CategoryPage
from search.serializers import (ElasticProductPageSerializer,
                                ElasticProductPageCustomSerializer,
                                ElasticCategoryCustomSerializer)
from search.indexes import ProductPageIndex, CategoryIndex
from search.constants import INDEX_SETTINGS, MAPPING_SETTINGS, CATEGORY_MAPPING

ELASTICSEARCH_URL = settings.ELASTICSEARCH_URL
ELASTICSEARCH_SNAPSHOT_REPO = settings.ELASTICSEARCH_SNAPSHOT_REPO
ELASTICSEARCH_SNAPSHOT_NAME = settings.ELASTICSEARCH_SNAPSHOT_NAME
ELASTICSEARCH_SNAPSHOT_DIR = settings.ELASTICSEARCH_SNAPSHOT_DIR


@app.task
def update_es_product(uuid):
    instance = ProductPage.objects.get(id=uuid)
    document = ElasticProductPageCustomSerializer(instance)
    document.save()


@app.task
def delete_es_product(uuid):
    """
    Чтобы избежать лишнего запроса к бд при сериализации в DocType
    и возможности отсутствия записи в бд при отложенном вызове
    удаляем запись из es-индекса напрямую
    """
    index = ProductPageIndex.index
    doc_type = ProductPageIndex._doc_type.name
    es = connections.get_connection(es_client)
    response = es.delete(
        index=index,
        doc_type=doc_type,
        id=uuid
    )
    return response


@app.task
def setup_settings():
    index = ProductPageIndex.index
    doc_type = ProductPageIndex._doc_type.name
    category_doc_type = CategoryIndex._doc_type.name

    index_url = '{0}{1}'.format(ELASTICSEARCH_URL, index)
    mapping_url = '{0}/{1}/_mapping'.format(index_url, doc_type)
    category_mapping_url = '{0}/{1}/_mapping'.format(index_url, category_doc_type)

    requests.delete(index_url)
    requests.put(index_url, json=INDEX_SETTINGS)
    requests.put(category_mapping_url, json=CATEGORY_MAPPING)
    requests.put(mapping_url)

@app.task
def rewrite_products():
    for instance in ProductPage.objects.all():
        try:
            document = ElasticProductPageCustomSerializer(instance)
            document.save()
        except:
            pass

@app.task
def rewrite_categories():
    for instance in CategoryPage.objects.all():
        try:
            document = ElasticCategoryCustomSerializer(instance)
            document.save()
        except:
            pass


@app.task
def rewrite_index():
    rewrite_products()
    rewrite_categories()


@app.task
def create_snapshot():
    index = ProductPageIndex.index
    repo_url = "{ELASTICSEARCH_URL}_snapshot/{SNAPSHOT_REPO}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        SNAPSHOT_REPO=ELASTICSEARCH_SNAPSHOT_REPO
    )
    snapshot_url = "{repo_url}/{SNAPSHOT_NAME}".format(
        repo_url=repo_url,
        SNAPSHOT_NAME=ELASTICSEARCH_SNAPSHOT_NAME
    )
    snapshot_config = {
        "indices": index,
        "type": "fs",
        "settings": {
            "compress": True,
            "location": ELASTICSEARCH_SNAPSHOT_DIR
        }
    }
    response = requests.post(url=repo_url, json=snapshot_config)
    response = requests.post(url=snapshot_url, json=snapshot_config)


@app.task
def restore_index_from_snapshot():
    index = ProductPageIndex.index
    doc_type = ProductPageIndex._doc_type.name

    index_url = "{ELASTICSEARCH_URL}{index}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        index=index
    )
    mapping_url = "{index_url}/{doc_type}".format(
        index_url=index_url,
        doc_type=doc_type
    )
    repo_url = "{ELASTICSEARCH_URL}_snapshot/{SNAPSHOT_REPO}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        SNAPSHOT_REPO=ELASTICSEARCH_SNAPSHOT_REPO
    )
    snapshot_url = "{repo_url}/{SNAPSHOT_NAME}".format(
        repo_url=repo_url,
        SNAPSHOT_NAME=ELASTICSEARCH_SNAPSHOT_NAME
    )
    url = snapshot_url+'/_restore/'
    response = requests.post(index_url+"/_close")
    response = requests.post(url=url)
    status_code = response.status_code
    response = requests.post(index_url+"/_open")
    return status_code


@app.task
def clear_snapshot():
    url = "{ELASTICSEARCH_URL}_snapshot/{SNAPSHOT_REPO}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        SNAPSHOT_REPO=ELASTICSEARCH_SNAPSHOT_REPO
    )
    response = requests.delete(url=url)
    dirname = ELASTICSEARCH_SNAPSHOT_DIR
    items = os.listdir(dirname)
    for item in items:
        try:
            os.remove(dirname+item)
        except IsADirectoryError:
            shutil.rmtree(dirname+item)


@app.task
def sync_elasticsearch():
    index = ProductPageIndex.index
    doc_type = ProductPageIndex._doc_type.name

    index_url = "{ELASTICSEARCH_URL}{index}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        index=index
    )
    mapping_url = "{index_url}/{doc_type}".format(
        index_url=index_url,
        doc_type=doc_type
    )
    repo_url = "{ELASTICSEARCH_URL}_snapshot/{SNAPSHOT_REPO}".format(
        ELASTICSEARCH_URL=ELASTICSEARCH_URL,
        SNAPSHOT_REPO=ELASTICSEARCH_SNAPSHOT_REPO
    )
    snapshot_url = "{repo_url}/{SNAPSHOT_NAME}".format(
        repo_url=repo_url,
        SNAPSHOT_NAME=ELASTICSEARCH_SNAPSHOT_NAME
    )

    index_exists = False
    counts_matches = False
    snapshot_exists = False

    index_response = requests.get(url=mapping_url+'/_count')
    if index_response.status_code == 200:
        index_exists = True
        doc_count = json.loads(index_response.text)['count']
        
    if index_exists is False:
        setup_settings()
        rewrite_index()
        pass

    else:
        products_count = ProductPage.objects.all().count()
        if doc_count == products_count:
            counts_matches = True
        else:
            rewrite_index()
        pass

    clear_snapshot()
    create_snapshot()


@app.task
def total_reindex():
    clear_snapshot()
    setup_settings()
    rewrite_index()
    create_snapshot()


# app.add_periodic_task(
#     crontab(minute=0,  hour='*/2'),
#     sync_elasticsearch.s(),
#     name='sync_elasticsearch',
# )


@app.task
def write_search_record(query, view):
    log_file = settings.SEARCH_LOGS_DIR + 'log.txt'
    date = datetime.datetime.now()
    line = "{query}, {view}, {date}\n".format(
        query=query,
        view=view,
        date=str(date)
    )

    with open(log_file, 'a') as fp:
        fp.write(line)


@beat_init.connect
def configure_elasticsearch(**kwargs):
    sync_elasticsearch.delay()
