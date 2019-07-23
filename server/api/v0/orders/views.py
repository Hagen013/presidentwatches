from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


from cart.models import Order
from cart.serializers import OrderPrivateSerializer

from api.views import ModelViewSet


class CustomOrdersFilter(filters.BaseFilterBackend):
    
    def filter_queryset(self, request, qs, view):
        params  = request.query_params
        public_id = params.get('public_id', None)
        phone     = params.get('phone', None)
        name      = params.get('name', None)
        email     = params.get('email', None)

        if public_id is not None:
            qs = qs.filter(
                public_id__icontains=public_id
            )

        if name is not None:
            qs = qs.filter(
                customer__name__icontains=name
            )

        if phone is not None:
            qs = qs.filter(
                customer__phone__icontains=phone
            )

        if email is not None:
            qs = qs.filter(
                customer__email__icontains=email
            )
        return qs


class OrderViewSet(ModelViewSet):

    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderPrivateSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        CustomOrdersFilter,
        filters.OrderingFilter
    )

    filter_fields = (
    )
    search_fields = (
    )
    ordering_fields = (
        '_order',
    )
