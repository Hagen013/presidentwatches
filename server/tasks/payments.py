from celery.schedules import crontab
from config.celery import app

from core.mail import Mail

from cart.models import Order
from payments.models import Payment

BASE_URL = 'http://localhost:8080'


@app.task
def notify(payment_id):
    instance = Payment.objects.get(
        id=payment_id
    )
    user = instance.user
    order = instance.order

    context = {
        'order': order,
        'payment': instance,
        'user': user,
        'BASE_URL': BASE_URL
    }

    template = 'mail/payment.html'
    title = 'Подтверждение оплаты заказа № {public_id}'.format(
        public_id=order.public_id
    )
    mail = Mail(
        title=title,
        template=template,
        recipient=user.email,
        context=context
    )
    mail.send()


@app.task
def notify_new_user(payment_id, password):
    instance = Payment.objects.get(
        id=payment_id
    )
    user = instance.user
    order = instance.order
    print('Полученный пароль')
    print(password)

    context = {
        'order': order,
        'payment': instance,
        'user': user,
        'BASE_URL': BASE_URL,
        'password': password
    }

    template = 'mail/payment-new-user.html'
    title = 'Подтверждение оплаты заказа № {public_id}'.format(
        public_id=order.public_id
    )
    mail = Mail(
        title=title,
        template=template,
        recipient=user.email,
        context=context
    )
    mail.send()

