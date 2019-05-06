from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import KladrSerializer, KladrDetalSerializer
from kladr.models import Kladr


class DetalKladrAPIView(APIView):

    def get(self, request, code=None, format=None):
        if not code:
            serializer = KladrSerializer(Kladr.subjects.all(), many=True)
        else:
            serializer = KladrDetalSerializer(Kladr.actual.get(code=code))
        return Response(serializer.data)


class SearchKladrAPIView(APIView):

    def get(self, request, line=None):
        serializer = KladrSerializer(
            Kladr.actual.filter(name__icontains=line).order_by('-houses_num')[:50],
            many=True
        )
        return Response(serializer.data)
