from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import pandas as pd
import numpy as np

from shop.models import ProductPage as Product
from shop.models import CategoryPage as Node
from shop.models import Attribute
from shop.models import AttributeValue as Value

from shop.utils import get_rows_from_file

df = pd.read_excel('kategorii.xlsx')
data = get_rows_from_file('data.json')
products_rows = data['products']

slugs = ['collection', 'series', 'country']
qs = Attribute.objects.filter(key__in=slugs)
qs.update(strict_options=False)

# Коллекция
attribute = Attribute(
    name='Коллекция',
    datatype=6,
    key='collection'
)
attribute.full_clean()
attribute.save()

# Страна
attribute = Attribute(
    name='Страна',
    datatype=5,
    key='country'
)
attribute.full_clean()
attribute.save()

# Серия
attribute = Attribute(
    name='Серия',
    datatype=5,
    key='series'
)
attribute.full_clean()
attribute.save()

qs = Node.objects.all().exclude(id__in=[Node.objects.first().id])
qs.delete()

exceptions = ['Коллекция', 'Страна', 'Серия']

with transaction.atomic():
    for index, row in df.iterrows():
        title = row['Title']
        slug = row['SLUG']
        attributes = row['Attributes']

        instance = Node(
            _title=title,
            slug=slug,
        )

        instance.full_clean()
        instance.save()

        attrs_pairs = attributes.split(';')
        for attr_pair in attrs_pairs:
            attribute_values_pair = attr_pair.split('#')
            attribute_name = attribute_values_pair[0]
            values_string = attribute_values_pair[1]
            values_names = values_string.split(',')

            try:
                attribute = Attribute.objects.get(
                    name=attribute_name
                )
                if attribute_name in exceptions:
                    for value_name in values_names:
                        value = Value.objects.get_or_create(
                            attribute,
                            value_name
                        )
                        instance.add_value(value)
            except ObjectDoesNotExist:
                pass


Node.objects.rebuild()