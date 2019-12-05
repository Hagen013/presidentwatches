import requests
import random

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from config.celery import app

from shop.models import ProductPage as Product
from users.models import UserMarketingGroup as Group
from cart.models import Promocode, PromocodeType, GiftSalesTable
from core.mail import Mail

from django.contrib.auth import get_user_model

User = get_user_model()


if settings.DEBUG:
    BASE_URL = 'http://localhost:8080'
else:
    BASE_URL = 'https://presidentwatches.ru'


def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    code = 'PW' + code
    return code


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


@app.task
def label_gift_prices():
    sales = GiftSalesTable.objects.first().sales
    brands = set(sales.keys())
    Product.objects.all().update(has_gift_price=False)
    Product.objects.filter(brand__in=brands).update(has_gift_price=True)


@app.task
def send_gift_price(user_pk, product_pk, password=None):
    template_name = 'mail/gift-price.html'

    user = User.objects.get(pk=user_pk)
    product = Product.objects.get(model=product_pk)
    sales = GiftSalesTable.objects.first().sales

    for i in range(100):
        code = get_promo_code(6)
        try:
            instance = Promocode.objects.get(
                name=code
            )
        except ObjectDoesNotExist:
            instance = Promocode(
                name=code,
                datatype=PromocodeType.Gift,
                sales=sales,
                has_limited_use=True
            )
            instance.save()
            break

    multiplier = sales.get(product.brand)
    percentage = multiplier * 100
    sale_amount = product._price * multiplier

    context = {
        'BASE_URL': BASE_URL,
        'email': user.email,
        'user': user,
        'password': password,
        'promocode': instance,
        'product': product,
        'percentage': percentage,
        'sale_amount': sale_amount
    }

    mail = Mail(
        title='Подарочный промокод',
        template=template_name,
        recipient=user.email,
        context=context
    )
    mail.send()