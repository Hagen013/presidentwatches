from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Order
from payments.models import Payment
from payments.serializers import PaymentSeializer, CreatePaymentSerializer


User = get_user_model()


class PaymentsListAPIView(APIView):

    serializer_class = PaymentSeializer

    def get(self, request, *args, **kwargs):
        qs = Payment.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        return Response({})


class PaymentsDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({})