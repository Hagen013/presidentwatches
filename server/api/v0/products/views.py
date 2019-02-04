from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from api.views import ModelViewSet
from shop.models import ProductPage
from shop.serializers import ProductPageSerializer, AttributeValueSerializer
from shop.models import AttributeValue as Value


class ProductPageViewSet(ModelViewSet):

    model = ProductPage
    queryset = ProductPage.objects.all()
    serializer_class = ProductPageSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = (
        'is_published',
        'is_in_stock'
    )
    search_fields = (
        'name',
    )
    ordering_fields = (
        'id',
        'scoring',
        '_price',
        'old_price'
        'created_at',
        'modified_at'
    )


class ProductValuesViewSet(viewsets.ViewSet):

    parent_model = ProductPage
    model = Value
    serializer_class = AttributeValueSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    def get_instance(self, product_pk):
        try:
            return self.parent_model.objects.get(
                id=product_pk
            )
        except ObjectDoesNotExist:
            raise Http404
        
    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        return self.model.objects.filter(
            product_set=product_pk
        )

    def filter_queryset(self, qs):
        for backend in list(self.filter_backends):
            qs = backend().filter_queryset(self.request, qs, self)
        return qs

    def paginate_queryset(self, qs, request):
        self.paginator = self.pagination_class()
        paginated_qs = self.paginator.paginate_queryset(qs, request)
        return paginated_qs


    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)

    def list(self, request, product_pk):
        qs = self.filter_queryset(self.get_queryset())
        qs = self.paginate_queryset(qs, request)
        serializer = self.serializer_class(qs, many=True)
        response = self.get_paginated_response(serializer.data)
        return response

    def create(self, request, product_pk):
        data = request.data

        import pickle
        with open('values.pickle', 'wb') as fp:
            pickle.dump(data, fp)

        queryparams = request.query_params
        bulk_mode = queryparams.get('bulk', False)
        if bulk_mode:
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                instance = self.get_instance(product_pk)

                instance.update_values_from_list(data)
                output = self.serializer_class(
                    instance.attribute_values.all(),
                    many=True
                )
                return Response(
                    {'results': output.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST
                )
        else:
            pass
        return Response({})

    def retrieve(self, product_pk, pk):
        return Response({})

    def update(self, product_pk, pk=None):
        return Response({})

    def delete(self, product_pk, pk):
        return Response({})
