from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Promocode
from cart.serializers import PromocodeSerializer


class SearchByNamePromocodeAPIView(APIView):

    model            = Promocode
    serializer_class = PromocodeSerializer

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', None)
        if name is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instance = self.model.objects.get(
                name=name
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )