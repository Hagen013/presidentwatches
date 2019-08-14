import requests

from django.conf import settings
from config.celery import app

from cart.models import Order


@app.task
def sms_notify(order_id):
    instance = Order.objects.get(public_id=order_id)
    to = instance.customer["phone"]
    msg = "ПрезидентВотчес.Ру: Ваш заказ принят под номером {order_id}. С Вами свяжется оператор для подтверждения заказа. Наш телефон: +74951775736".format(
        order_id=order_id
    )
    payload = {
        "api_id": settings.SMS_SECRET_KEY,
        "msg": msg,
        "to": to,
        "from": "PWatches",
        "json": "1"
    }
    response = requests.get(url=settings.SMS_URL, params=payload)
    if response.json()["status"] != "OK":
        raise Error("SMS notification failed")
    else:
        instance.notified_by_sms = True
        instance.save()
