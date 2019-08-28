from django.db import transaction

from shop.models import ProductPage as Product


def update_descriptions():
    with transaction.atomic():
        for instance in Product.objects.all():
            instance.description = instance.description.replace('http://presidentwatches.ru', '')
            instance.save()