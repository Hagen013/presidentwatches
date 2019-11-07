import requests

from django.conf import settings
from django.db import transaction

from config.celery import app

from shop.models import ProductPage as Product
from users.models import UserMarketingGroup as Group


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


