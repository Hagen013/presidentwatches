from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.es_client import es_client


class FacetesApiView(APIView):

    def get(self, request):
        slug = request.GET.get("key")
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

        return Response(response)

