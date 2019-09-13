# import uuid

# from django.db import models
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import JSONField

# from djchoices import DjangoChoices, ChoiceItem
# from yandex_checkout.client import ApiClient
# from yandex_checkout.domain.request.payment_request import PaymentRequest

# from cart.models import Order

# User = get_user_model()

# API_URL = settings.YANDEX_KASSA_API
# SHOP_ID = settings.YANDEX_KASSA_SHOP_ID
# SECRET  = settings.YANDEX_KASSA_SECRET


# class PaymentStatuses(DjangoChoices):

#     Pending = ChoiceItem('pending', 'В обработке')
#     Success = ChoiceItem('success', 'Успешно')
#     Failed  = ChoiceItem('failed', 'Ошибка')


# class Payment(models.Model):

#     class Meta:
#         abstract=True

#     base_path = '/payments'

#     user = models.ForeignKey(
#         User,
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#         related_name='payments'
#     )

#     order = models.ForeignKey(
#         Order,
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE
#     )

#     y_id = models.CharField(
#         max_length=64
#     )

#     status = models.CharField(
#         choices=PaymentStatuses.choices,
#         default=PaymentStatuses.Pending,
#         max_length=32
#     )

#     paid = models.BooleanField(
#         default=False
#     )

#     amount = models.FloatField(
#         default=0
#     )

#     amount_paid = models.FloatField(
#         default=0
#     )

#     confirmation_url = models.CharField(
#         max_length=256,
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     description = models.CharField(
#         max_length=256,
#     )

#     metadata = JSONField(
#         default=dict
#     )

#     refundable = models.CharField(
#         default=True
#     )

#     def __init__(self):
#         self.client = ApiClient()

#     @classmethod
#     def create(cls, params, idempotency_key=None):
#         instance = cls()
#         path = cls.base_path

#         if not idempotency_key:
#             idempotency_key = uuid.uuid4()

#         headers = {
#             'Idempotence-Key': str(idempotency_key)
#         }

#         if isinstance(params, dict):
#             params_object = PaymentRequest(params)
#         elif isinstance(params, PaymentRequest):
#             params_object = params
#         else:
#             raise TypeError('Invalid params value type')

#         response = instance.client.request(HttpVerb.POST, path, None, headers, params_object)
        
#         instance.y_id = response['id']
#         instance.status = response['status']
#         instance.paid = response['paid']
#         instance.amount_paid = response['amount']['value']
#         confirmation_url = response['confirmation_url']