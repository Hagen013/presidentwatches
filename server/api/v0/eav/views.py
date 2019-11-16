from django.db import models

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.views import ModelViewSet, ListViewMixin
from shop.models import Attribute, AttributeGroup, AttributeValue
from shop.models import ProductValueRelation as Relation
from shop.serializers import (AttributeSerializer,
                              AttributeGroupSerializer,
                              AttributeValueSerializer,
                              AttributeValueProductsCountSerializer)


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
        'is_filter',
        'key'
    )
    search_fields = (
        'name',
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
        'attribute__key',
    )
    search_fields = (
    )
    ordering_fields = (
        'id',
    )


class APIViewValueSetProductCountsView(APIView):

    model            = AttributeValue
    queryset         = AttributeValue.objects.all()
    serializer_class = AttributeValueProductsCountSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = (
        'attribute__key',
    )
    search_fields = (
    )
    ordering_fields = (
        'id',
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def filter_queryset(self, qs):
        for backend in list(self.filter_backends):
            qs = backend().filter_queryset(self.request, qs, self)
        qs = qs.annotate(products_count=models.Count('product_set', filter=models.Q(product_set__is_in_stock=True)))
        return qs

    def paginate_queryset(self, qs, request):
        self.paginator = self.pagination_class()
        paginated_qs = self.paginator.paginate_queryset(qs, request)
        return paginated_qs

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)

    def list(self, request):
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(qs, many=True)
        return Response({
            'results': serializer.data
        })
