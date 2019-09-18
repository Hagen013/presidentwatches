import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

from djchoices import DjangoChoices, ChoiceItem
from yandex_checkout.domain.common.http_verb import HttpVerb
from yandex_checkout import Configuration
from yandex_checkout.client import ApiClient
from yandex_checkout.domain.request.payment_request import PaymentRequest

from cart.models import Order

User = get_user_model()

API_URL = settings.YANDEX_KASSA_API
SHOP_ID = settings.YANDEX_KASSA_SHOP_ID
SECRET  = settings.YANDEX_KASSA_SECRET

Configuration.account_id = SHOP_ID
Configuration.secret_key = SECRET


class PaymentStatuses(DjangoChoices):

    Pending = ChoiceItem('pending', 'В обработке')
    Success = ChoiceItem('success', 'Успешно')
    Failed  = ChoiceItem('failed', 'Ошибка')


class Payment(models.Model):

    class Meta:
        abstract=False
        ordering = ['created_at',]

    base_path = '/payments'

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='payments'
    )

    order = models.ForeignKey(
        Order,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    y_id = models.CharField(
        max_length=64
    )

    uuid = models.CharField(
        max_length=64
    )

    status = models.CharField(
        choices=PaymentStatuses.choices,
        default=PaymentStatuses.Pending,
        max_length=32
    )

    paid = models.BooleanField(
        default=False
    )

    amount = models.FloatField(
        default=0
    )

    amount_paid = models.FloatField(
        default=0
    )

    confirmation_url = models.CharField(
        max_length=256,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    description = models.CharField(
        max_length=256,
    )

    metadata = JSONField(
        default=dict,
        blank=True
    )

    refundable = models.BooleanField(
        default=True
    )

    def __init__(self, *args, **kwargs):
        self.client = ApiClient()
        super(Payment, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, params, idempotency_key=None, user=None, order=None):
        
        instance = cls()
        path = cls.base_path

        if not idempotency_key:
            idempotency_key = uuid.uuid4()

        instance.uuid = idempotency_key

        headers = {
            'Idempotence-Key': str(idempotency_key)
        }

        if isinstance(params, dict):
            params_object = PaymentRequest(params)
        elif isinstance(params, PaymentRequest):
            params_object = params
        else:
            raise TypeError('Invalid params value type')

        response = instance.client.request(HttpVerb.POST, path, None, headers, params_object)
        
        instance.y_id = response['id']
        instance.status = response['status']
        instance.paid = response['paid']
        instance.amount = response['amount']['value']
        instance.confirmation_url = response['confirmation']['confirmation_url']
        instance.created_at = response['created_at']
        instance.description = response['description']
        instance.metadata = response['metadata']
        instance.refundable = response['refundable']

        instance.user = user
        instance.order = order

        instance.full_clean()
        instance.save()

        return instance