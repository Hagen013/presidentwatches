from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination


class ListViewMixin():

    model = None
    serializer_class = None

    filter_fields = ()
    search_fields = ()
    ordering_fields = ()

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    def get_queryset(self):
        return self.model.objects.all()

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

    def list(self, request):
        qs = self.filter_queryset(self.get_queryset())
        qs = self.paginate_queryset(qs, request)
        serializer = self.serializer_class(qs, many=True)
        response = self.get_paginated_response(serializer.data)
        return response


class ModelViewSet(ListViewMixin, viewsets.ViewSet):
    """
    Custom default model ViewSet class
    """
    def get_instance(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404


    def create(self, request):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, pk):
        instance = self.get_instance(pk)
        serializer = self.serializer_class(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def update(self, request, pk):
        instance = self.get_instance(pk)
        serializer = self.serializer_class(
            instance,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        instance = self.get_instance(pk)
        instance.delete()
        return Response(
            status=status.HTTP_200_OK
        )
