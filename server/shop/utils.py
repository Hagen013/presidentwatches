import json

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from .models import ProductPage
from .serializers import ProductPageJsonSerializer as JsonSerializer
from .serializers import ProductPageSerializer as Serializer


def get_rows_from_file(filename):
    data = []
    categories = []
    products = []

    with open(filename, 'r') as fp:
        for line in fp:
            data.append(line)

    for line in data:
        instance = json.loads(line)
        fields = instance.get('fields', None)
        if fields is not None:
            price = fields.get('price', None)
            if price is not None:
                products.append(instance)
            else:
                categories.append(instance)
        else:
            categories.append(instance)
            
    return {
        'categories': categories,
        'products': products
    }


def populate_db_from_json(filename):
    ProductPage.objects.all().delete()
    data = get_rows_from_file(filename)
    products_rows = data['products']
    with transaction.atomic():
        for product in products_rows:
            data = JsonSerializer(product).data
            serializer = Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValidationError('Invalid product data')

