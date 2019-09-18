from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from cart.models import Order
from payments.models import Payment
from payments.serializers import PaymentSeializer, CreatePaymentSerializer


User = get_user_model()


class PaymentsListAPIView(APIView):

    serializer_class = PaymentSeializer
    permissions_class = permissions.IsAdminUser

    filter_fields = ('order', 'user')

    def filter_queryset(self, qs):
        for field in self.filter_fields:
            value = self.request.GET.get(field, None)
            if value is not None:
                lookup = {
                    field: value
                }
                qs = qs.filter(**lookup)
        return qs

    def get(self, request, *args, **kwargs):
        qs = Payment.objects.all()
        qs = self.filter_queryset(qs)
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


class CreatePaymentAPIView(APIView):

    serializer_class = PaymentSeializer

    def post(self, request, *args, **kwargs):
        data = request.data

        order_pk = data.get('order', None)
        user_pk = data.get('user', None)
        email = data.get('email', None)

        user_created = False

        order = None

        try:
            order = Order.objects.get(
                pk=order_pk
            )
        except ObjectDoesNotExist:
            return Response(
                'Заказ не найден',
                status=status.HTTP_404_NOT_FOUND
            )

        user = None
        if order.user is not None:
            if user_pk != order.user.id:
                return Response(
                    'Переданный ID пользователя и ID пользователя заказа не совпадают',
                    status=status.HTTP_BAD_REQUEST
                )
            else:
                try:
                    user = User.objects.get(id=user_pk)
                except ObjectDoesNotExist:
                    return Response(
                        'Пользователь с таким ID не найден'
                    )

        # 1. Есть заказ
        # 2. Нет юзера
        if user is None:
            try:
                user = User.objects.get(
                    email=email
                )
            except ObjectDoesNotExist:
                pass

            # Всё еще не найден
            if user is None:
                password = User.objects.make_random_password()

                user = User(
                    email=email,
                    username=email,
                    password=password
                )
                try:
                    user.full_clean()
                    user.save()
                except ValidationError:
                    return Response(
                        'Недопустимые данные',
                        status=status.HTTP_BAD_REQUEST
                    )

                # 1. Есть заказ
                # 2. Есть новый юзер
                user_created = True
            else:
                # 1. Есть заказ
                # 2. Есть найденный юзер
                order.user = user
                order.save()

        # 1. Есть заказ
        # 2. Есть переданный юзер
        else:
            pass

        return_url = 'https://presidentwatches/payments/confirmation/{uuid}'.format(
            uuid=order.uuid
        )
        description = 'Заказ №{public_id}'.format(
            public_id=order.public_id
        )

        params = {
            'amount': {
                'value': order.total_price,
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': return_url
            },
            'capture': True,
            'description': description
        }


        payment = Payment.create(
            params,
            order=order,
            user=user
        )

        serializer = self.serializer_class(
            payment
        )

        if user_created:
            # Если создали нового юзера - отправляем ссылку с авто-аутентификацией
            pass
        else:
            # Если не создавали - просто ссылку с редиректом на платежи.
            pass

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
