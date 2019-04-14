from django.conf import settings

from elasticsearch import Elasticsearch, RequestsHttpConnection


es_client = Elasticsearch(
    hosts=[settings.ELASTICSEARCH_URL],
    connection_class=RequestsHttpConnection
)
