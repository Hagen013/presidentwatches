import os
import time

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from shop.models import ProductPage as Product
from shop.models import AttributeValue as Value

YML_FILEPATH = settings.YML_PATH + 'moy_sklad_buffer.xml'
YML_FILEPATH_ORIGIN = settings.YML_PATH + 'moy_sklad.xml'


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def get_yml_node(instance):
    try:
        brand = instance.attribute_values.get(attribute__name='Бренд')
    except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
        try:
            brand = Value.objects.get(
                attribute__name='Бренд',
                value_enum=instance.brand
            )
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            brand = None
    if brand is not None:
        return {
            'id': brand.id,
            'name': brand.value
        }
    return {
        'id': 10005,
        'name': 'Каталог наручных часов'
    }


@app.task
def generate_yml_file(delay=60):
    touch(YML_FILEPATH)
    products = Product.objects.all()
    brands = Value.objects.filter(attribute__name='Бренд')
    date = now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M')
    filtered = []
    for product in products:
        if product.has_image:
            filtered.append(product)
    products = filtered

    context = {
        'date': date,
        'nodes': brands,
        'products': products,
        'get_yml_node': get_yml_node,
        'base_url': 'https://presidentwatches.ru'
    }

    xml_raw = render_to_string(
        template_name="api/yml.xml",
        context=context
    )

    with open(YML_FILEPATH, "w") as fp:
        fp.write(xml_raw)

    time.sleep(delay)
    os.rename(YML_FILEPATH, YML_FILEPATH_ORIGIN)


app.add_periodic_task(
    crontab(minute="01", hour='07'),
    generate_yml_file.s(),
    name='generate_yml_file',
)
