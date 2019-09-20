import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import JSONParser

from cart.models import Order
from payments.models import Payment
from payments.serializers import PaymentSeializer, CreatePaymentSerializer
from tasks.payments import notify, notify_new_user
from .permissions import IsAdminOrOwner


User = get_user_model()


class PaymentsListAPIView(APIView):

    serializer_class = PaymentSeializer
    permissions_class = IsAdminOrOwner

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


Y_KASSA_EVENTS_MAP = {
    'payment.waiting_for_capture': 'pending',
    'payment.succeeded': 'success',
    'payment.canceled': 'failed',
    'refund.succeeded': 'refund'
}


class PaymentsNotificationsAPIView(APIView):


    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        y_id = data['object']['id']
        event = data['event']

        try:
            instance = Payment.objects.get(
                y_id=y_id
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        instance.status = Y_KASSA_EVENTS_MAP.get(event)
        instance.paid = data['object']['paid']
        instance.amount_paid = data['object']['amount']['value']
        instance.resolvet_at = timezone.now()
        order = instance.order
        order.payment['paid'] = True
        order.payment['amount'] = instance.amount_paid
        instance.save()
        return Response(
            status=status.HTTP_200_OK
        )


class CreatePaymentAPIView(APIView):

    serializer_class = PaymentSeializer
    permissions_class = permissions.IsAdminUser

    def post(self, request, *args, **kwargs):
        data = request.data

        order_pk = data.get('order', None)
        user_pk = data.get('user', None)
        email = data.get('email', None)
        phone = data.get('phone', None).replace('+', '')
        name = data.get('name')

        user_created = False
        password = None

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
                    status=status.HTTP_400_BAD_REQUEST
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
                    user.set_password(password)
                    user.save()
                except ValidationError:
                    return Response(
                        'Недопустимые данные',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 1. Есть заказ
                # 2. Есть новый юзер
                user_created = True
                order.user = user
                order.save()
            else:
                # 1. Есть заказ
                # 2. Есть найденный юзер
                order.user = user
                order.save()

        # 1. Есть заказ
        # 2. Есть переданный юзер
        else:
            pass

        return_url = 'https://presidentwatches.ru/u/profile/#payments'.format(
            uuid=order.uuid
        )
        description = 'Заказ №{public_id}'.format(
            public_id=order.public_id
        )

        receipt = {
            'phone': phone,
            'email': email,
            'items': [],
        }

        for item in order.cart['items'].values():
            descr = "{brand} {model}".format(
                brand=item['brand'],
                model=item['model']
            )
            receipt['items'].append({
                'description': descr,
                'quantity': item['quantity'],
                'amount': {
                    'value': item['price'],
                    'currency': 'RUB'
                },
                'vat_code': '1',
                'payment_mode': 'full_prepayment',
                'payment_subject': 'commodity'
            })

        
        try:
            delivery_price = order.delivery['price']
        except:
            delivery_price = None

        if delivery_price is not None:
            if delivery_price > 0:
                receipt['items'].append({
                    'description': 'Доставка',
                    'quantity': 1,
                    'amount': {
                        'value': delivery_price,
                        'currency': 'RUB'
                    },
                    'vat_code': '1',
                    'payment_mode': 'full_prepayment',
                    'payment_subject': 'commodity'
                })

        params = {
            'amount': {
                'value': order.total_price,
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': return_url
            },
            'receipt': receipt,
            'capture': True,
            'description': description
        }

        payment = Payment.create(
            params,
            order=order,
            user=user
        )

        if user_created:
            notify_new_user.delay(payment.id, password=password)
        else:
            notify.delay(payment.id)

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
            {
                'payment': serializer.data,
                'user': user.id
            },
            status=status.HTTP_201_CREATED
        )
