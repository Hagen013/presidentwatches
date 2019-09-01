import os
from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser 
from django_filters.rest_framework import DjangoFilterBackend

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from api.views import ModelViewSet
from shop.serializers import (ProductPageSerializer,
                              AttributeValueSerializer,
                              ProductImageSerializer,
                              ProductImageFileSerializer)

from shop.models import Attribute
from shop.models import ProductImage
from shop.models import AttributeValue as Value
from shop.models import ProductPage as Product
from shop.models import ProductValueRelation as Relation


class ProductPageEAVFilterBackend():

    def __init__(self):
        self.filters = self.get_filters()
        self.filters_keys = [f.key for f in self.filters]

    def get_filters(self):
        return Attribute.objects.filter(is_filter=True)

    def filter_queryset(self, request, qs, view):
        for key, values in request.GET.items():
            if key in self.filters_keys:
                values = [v for v in values.split(',')]
                unfilled = False
                values = set(values)
                if 'none' in values:
                    unfilled = True
                    values.remove('none')
                if len(values) == 0 and unfilled:
                    qs = qs.exclude(attribute_values__in=Attribute.objects.get(key=key).values)
                elif not unfilled:
                    qs = qs.filter(attribute_values__in=values)
                else:
                    qs = qs.filter(attribute_values__in=values).union(
                        qs.exclude(attribute_values__in=Attribute.objects.get(key=key).values)
                    )
        return qs


class ProductPageViewSet(ModelViewSet):

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductPageSerializer
    pagination_class = LimitOffsetPagination
    permissions_class = permissions.IsAdminUser


    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ProductPageEAVFilterBackend
    )

    filter_fields = (
        'is_published',
        'is_in_stock',
        'is_in_store'
    )
    search_fields = (
        'model',
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

    parent_model = Product
    model = Value
    serializer_class = AttributeValueSerializer
    pagination_class = LimitOffsetPagination
    permissions_class = permissions.IsAdminUser

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
        data = request.data['attributes']

        values_to_add = []
        values_to_remove = []

        received_attributes_ids = {attr['id'] for attr in data}

        attrs_to_remove = set()

        ids_to_add = set()
        ids_to_remove = set()

        instance = self.get_instance(product_pk)
        
        stored = instance.attribute_values.filter(attribute__id__in=received_attributes_ids)
        stored_map = defaultdict(set)
        for value in stored:
            stored_map[value.attribute.id].add(value.id)
            
        for attr in data:
            if attr['datatype'] == 6:
                value_set = set(attr['values'])
                to_add = value_set.difference(stored_map[attr['id']])
                to_remove = stored_map[attr['id']].difference(value_set)
                ids_to_add.update(to_add)
                ids_to_remove.update(to_remove)
            elif attr['datatype'] == 5:
                if attr['values'] not in stored_map[attr['id']]:
                    ids_to_add.add(attr['values'])
                    stored_value = list(stored_map[attr['id']])
                    if len(stored_value) > 0:
                        ids_to_remove.add(stored_value[0])
            elif attr['datatype'] == 4:
                value = attr['values']
                if value is not None:
                    attrs_to_remove.add(attr['id'])
                    attribute = Attribute.objects.get(id=attr['id'])
                    values_to_add.append(
                        Value.objects.get_or_create(
                            attribute=attribute,
                            value=attr['values']
                        )
                    )
                else:
                    attrs_to_remove.add(attr['id'])
            elif attr['datatype'] == 3 or attr['datatype'] == 2:
                attrs_to_remove.add(attr['id'])
                attribute = Attribute.objects.get(id=attr['id'])
                values_to_add.append(
                    Value.objects.get_or_create(
                        attribute=attribute,
                        value=attr['values']
                    )
                )
            else:
                value = attr['values']
                if len(value) == 0:
                    attrs_to_remove.add(attr['id'])
                else:
                    attrs_to_remove.add(attr['id'])
                    attribute = Attribute.objects.get(id=attr['id'])
                    values_to_add.append(
                        Value.objects.get_or_create(
                            attribute=attribute,
                            value=attr['values']
                        )
                    )

        with transaction.atomic():
            relations_to_delete = Relation.objects.filter(
                value_id__in=ids_to_remove,
                entity=instance
            ).union(Relation.objects.filter(
                value__attribute__id__in=attrs_to_remove,
                entity=instance
            ))

            for relation in relations_to_delete:
                relation.delete()
            
            qs_to_add = Value.objects.filter(
                id__in=ids_to_add
            )
            for value in qs_to_add:
                Relation(
                    value=value,
                    entity=instance
                ).save()
                
            for value in values_to_add:
                Relation(
                    value=value,
                    entity=instance
                ).save()

        return Response(status=status.HTTP_200_OK)

    def retrieve(self, product_pk, pk):
        return Response({})

    def update(self, product_pk, pk=None):
        return Response({})

    def delete(self, product_pk, pk):
        return Response({})


class ProductImagesAPIView(APIView):

    model            = ProductImage
    serializer_class = ProductImageSerializer
    permissions_class = permissions.IsAdminUser

    def get_instance(self, pk):
        try:
            return self.product_model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, product_pk):
        images = self.model.objects.filter(
            product=product_pk
        )
        serializer = self.serializer_class(images, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, product_pk):
        stored_images = self.model.objects.filter(
            product=product_pk
        )
        
        received_images = request.data
        received_images_mapping = {}
        for image in received_images:
            received_images_mapping[image['id']] = {
                'order': image['order']
            }

        with transaction.atomic():
            for image in stored_images:
                received = received_images_mapping.get(image.id, None)
                if received is None:
                    image.delete()
                else:
                    if image.order != received['order']:
                        image.order = received['order']
                        image.save()
        
        return Response({})


class ProductImageUploadView(APIView):

    model = Product
    permissions_class = permissions.IsAdminUser
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)

    def get_instance(self, pk):
        try:
            return self.model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404


    def put(self, request, pk):
        instance = self.get_instance(pk)
        imageFile = request.FILES.get('image', None)
        if imageFile is not None:
            fs = FileSystemStorage()
            filepath = '{MEDIA_ROOT}images/{model}/{name}'.format(
                MEDIA_ROOT=settings.MEDIA_ROOT,
                model=instance.model,
                name=imageFile.name
            )
            filename = fs.save(filepath, imageFile).replace(settings.MEDIA_ROOT, '')
            instance.image = filename
            instance.save()
            instance.image.close()
            instance.thumbnail.close()
        return Response({})


class ProductImagesUploadView(APIView):

    model = Product
    permissions_class = permissions.IsAdminUser
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)
    serializer_class = ProductImageFileSerializer

    def get_instance(self, pk):
        try:
            return self.model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, pk):
        instance = self.get_instance(pk)
        count = instance.images.count()
        files = request.FILES.keys()
        fs = FileSystemStorage()
        for key in files:
            count += 1
            image_file = request.FILES[key]
            serializer = self.serializer_class(instance, image_file, fs, count)
            serializer.save()
        data = ProductImageSerializer(instance.images.all(), many=True).data
        return Response(
            data,
            status=status.HTTP_200_OK
        )