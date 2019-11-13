import requests

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from config.celery import app

from shop.models import ProductPage as Product
from users.models import UserMarketingGroup as Group
from core.mail import Mail

from django.contrib.auth import get_user_model

User = get_user_model()


if settings.DEBUG:
    BASE_URL = 'http://localhost:8080'
else:
    BASE_URL = 'https://presidentwatches.ru'


@app.task
def label_club_prices():
    group = Group.objects.get(
        name='Зарегестрированные'
    )
    sales = group.sales
    all_sales = sales.get('all', None)
    if all_sales is not None and all_sales > 0:
        Product.objects.update(has_club_price=True)
    else:
        with transaction.atomic():
            for instance in Product.objects.all():
                sale = sales.get(instance.brand, None)
                if sale is not None and sale > 0:
                    instance.has_club_price = True
                    instance.save()
                else:
                    instance.has_club_price = False
                    instance.save()


@app.task
def notify_existing_user(pk, model):
    template = 'mail/club-price-existing.html'

    try:
        user = User.objects.get(
            pk=pk
        )
    except ObjectDoesNotExist:
        user = None

    if user is None:
        pass

    else:
        instance = Product.objects.get(model=model)
        instance.set_club_price(user.marketing_group)
        sale = round(((instance.price - instance.club_price) / instance.price) * 100)

        context = {
            'instance': instance,
            'user': user,
            'BASE_URL': BASE_URL,
            'return_url': instance.absolute_url,
            'sale': sale
        }

        mail = Mail(
            title='Клубная цена',
            template=template,
            recipient=user.email,
            context=context
        )
        mail.send()



@app.task
def notify_created_user(pk, model, password):
    template = 'mail/club-price-created.html'

    try:
        user = User.objects.get(
            pk=pk
        )
    except ObjectDoesNotExist:
        user = None

    if user is None:
        pass

    else:
        instance = Product.objects.get(model=model)
        instance.set_club_price(user.marketing_group)
        sale = round(((instance.price - instance.club_price) / instance.price) * 100)

        context = {
            'instance': instance,
            'user': user,
            'BASE_URL': BASE_URL,
            'return_url': instance.absolute_url,
            'sale': sale,
            'password': password
        }

        mail = Mail(
            title='Клубная цена',
            template=template,
            recipient=user.email,
            context=context
        )
        mail.send()



