from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Order


class OrdersListApiView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
        })


class OrderDetailApiView(APIView):

    def get(self, pk, *args, **kwargs):
        return Response({
        })