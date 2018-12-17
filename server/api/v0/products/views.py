from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from api.views import ModelViewSet
from shop.models import ProductPage
from shop.serializers import ProductPageSerializer


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
