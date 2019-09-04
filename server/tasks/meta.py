from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from shop.models import CategoryNodeOutdatedUrl as Outdated
from shop.models import CategoryPage as Node
from shop.models import ProductPage as Product

from shop.utils import get_rows_from_file


def update_meta():

    categories = get_rows_from_file('./data/pw_pages_190803.json')['categories']

    mapping = {}

    for row in categories:
        mapping[row['title']] = row

    not_found = []

    with transaction.atomic():
        for node in Node.objects.all():
            row = mapping.get(node.name, None)
            if row is None:
                not_found.append(node)
            else:
                meta_title = row.get('meta_title', None)
                meta_description = row.get('meta_description', None)
                
                if meta_title is not None:
                    node._meta_title = meta_title
                    
                if meta_description is not None:
                    node._meta_description =  meta_description
                    
                if meta_description is not None or meta_title is not None:
                    node.save()

    node = Node.objects.get(name='Каталог часов')
    node._meta_title = 'Каталог часов. Оригинальные часы. Широкий выбор наручных часов'
    node._meta_description = 'Широкий выбор оригинальных наручных часов на ПрезидентВотчес.Ру Полистайте каталог часов на нашем сайте, сделайте ваш выбор, купите часы до доступной цене. Интернет магазин ПрезидентВотчес.Ру +7 495 133 20 56'
    node.save()

    products = get_rows_from_file('./data/pw_pages_190803.json')['products']

    with transaction.atomic():

        for row in products:
            model = None
            fields = row.get('fields', None)
            if fields is not None:
                model = fields.get('model', None)

            if model is not None:
                try:
                    instance = Product.objects.get(model=model)

                    meta_title = fields.get('meta_title', None)
                    meta_description = fields.get('meta_description', None)

                    if meta_title is not None:
                        instance._meta_title = meta_title

                    if meta_description is not None:
                        instance._meta_description = meta_description

                    if meta_title is not None or meta_description is not None:
                        instance.save()

                except ObjectDoesNotExist:
                    pass