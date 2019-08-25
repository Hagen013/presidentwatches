from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.models import ProductPage as Product


class ProductImagesUploadView(APIView):

    model = Product

    def get_instance(self, pk):
        try:
            return self.model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404


    def post(self, requeset, pk):
        return Response({})
