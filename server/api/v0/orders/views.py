from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


from cart.models import Order
from cart.serializers import OrderPrivateSerializer

from api.views import ModelViewSet


class OrderViewSet(ModelViewSet):

    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderPrivateSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = (
    )
    search_fields = (
    )
    ordering_fields = (
    )
