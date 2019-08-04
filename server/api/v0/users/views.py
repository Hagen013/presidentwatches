from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from cart.models import Order
from cart.serializers import OrderSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserOrdersListApiView(APIView):

    model_class = Order
    serializer_class = OrderSerializer

    def get(self, request, user_pk):
        print(request.user)
        qs = self.model_class.objects.filter(user__pk=user_pk)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)


class UserOrderDetailsApiView(APIView):

    def get(self, request, user_pk, order_pk):
        return Response({
        })


class UserProfileApiView(APIView):

    def get(self, request, user_pk):
        return Response({
        })