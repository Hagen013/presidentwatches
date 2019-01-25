from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.views import ModelViewSet
from shop.models import Attribute, AttributeGroup, AttributeValue
from shop.serializers import (AttributeSerializer,
                              AttributeGroupSerializer,
                              AttributeValueSerializer)


class AttributeViewSet(ModelViewSet):

    model            = Attribute
    queryset         = Attribute.objects.all()
    serializer_class = AttributeSerializer
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
        'id',
    )


class AttributeGroupViewSet(ModelViewSet):

    model            = AttributeGroup
    queryset         = AttributeGroup.objects.all()
    serializer_class = AttributeGroupSerializer
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
        'id',
    )


class AttributeValueViewSet(ModelViewSet):

    model            = AttributeValue
    queryset         = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
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
        'id',
    )
