from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from cart.models import Order
from cart.serializers import OrderSerializer
from users.serializers import UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserOrdersListApiView(APIView):

    model_class = Order
    serializer_class = OrderSerializer

    def get(self, request, user_pk):
        qs = self.model_class.objects.filter(user__pk=user_pk)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)


class UserOrderDetailsApiView(APIView):

    def get(self, request, user_pk, order_pk):
        return Response({
        })


class UserProfileApiView(APIView):
    
    model = User
    serializer_class = UserSerializer

    def get(self, request, user_pk):

        try:
            instance = self.model.objects.get(
                pk=user_pk
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404)

        serializer = self.serializer_class(instance)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, user_pk):

        serializer = self.serializer_class(data=request.data, instance=request.user)
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
