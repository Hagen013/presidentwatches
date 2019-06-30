from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings

# from celery.signals import beat_init
# from celery.schedules import crontab
# from config.celery import app

from shop.models import ProductPage, CategoryPage

FILEPATH = settings.YML_PATH + "retail-rocket.xml"


def generate_yml_file():
    products = ProductPage.objects.all()
    categories = CategoryPage.objects.all()
    date = now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M')

    context = {
               'base_url': 'http://5.189.227.162', 
               'date': date,
               'categories': categories,
               'products': products,
               'get_product_category': lambda product: CategoryPage.objects.get_by_product(product)
               }

    xml_raw = render_to_string(
        template_name="api/retail-rocket.xml",
        context=context
    )

    with open(FILEPATH, "w") as fp:
        fp.write(xml_raw)