from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch

from config.es_client import es_client

from shop.models import AttributeValue
from shop.serializers import AttributeValuePublicSerializer
from search.patterns import generate_from_pattern


class SearchApiView(APIView):

    def get(self, request):
        query = request.GET.get('line', '')
        body = generate_from_pattern(query)
        response = es_client.search(
            index='store',
            doc_type='category,product',
            body=body
        )
        return Response(
            response['hits']['hits'],
            status=status.HTTP_200_OK
        )


class FacetesApiView(APIView):

    def get(self, request):
        slug = request.GET.get("key")

        values = AttributeValue.objects.filter(attribute__key=slug)
        serializer = AttributeValuePublicSerializer(values, many=True)


        fields = set(request.GET.keys()).difference({'key', slug})
        body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {"is_in_stock": "true"}
                        }
                    ]
                }
            },
            "aggs": {
                "facet": {
                    "terms": {"field": slug, "size": 200000}
                }
            }
        }

        for field in fields:
            values = request.GET.get(field).split(',')
            body['query']['bool']['must'].append({
                "terms": {
                    field: values
                }
            })

        response = es_client.search(
            index="store",
            doc_type="product",
            body=body
        )

        return Response({
            'counts': response['aggregations']['facet']['buckets'],
            'values': serializer.data,
        })


class FacetesCountApiView(APIView):

    def get(self, request, key):

        fields = set(request.GET.keys())

        body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {"is_in_stock": "true"}
                        }
                    ]
                }
            }
        }

        for field in fields:
            values = request.GET.get(field).split(',')
            body['query']['bool']['must'].append({
                "terms": {
                    field: values
                }
            })

        response = es_client.search(
            index="store",
            doc_type="product",
            body=body
        )
        
        return Response(
            response,
            status=status.HTTP_200_OK
        )
