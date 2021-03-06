from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings

from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from users.models import UserMarketingGroup as Group
from shop.models import Attribute
from shop.models import CategoryPage as Node
from shop.models import ProductPage as Product
from shop.models import AttributeValue as Value


FILEPATH = settings.YML_PATH + "retail-rocket.xml"


def get_nodes_by_product(qs, product):
    av = product.attribute_values.all()
    av_set = {v.id for v in av}
    nodes = []
    
    for node in qs:
        node_av = node.attribute_values.all()
        node_av_set = {v.id for v in node_av}
        difference = node_av_set.difference(av_set)
        if len(difference) == 0:
            nodes.append(node)
    
    ids = [node.id for node in nodes]
    qs = Node.objects.filter(id__in=ids).exclude(outputs__in=ids)
    return qs


def sorting_function(node):
    try:
        order = node.attribute_values.last().attribute.order
    except AttributeError:
        order = 0
    return (node._depth, order)


def club_prices(groups, instance):
    prices = []

    for group in groups:
        sale = group.sales.get(instance.brand, None)
        if sale is not None:
            price = round(((1-sale) * instance.price))
        else:
            price = instance.price
        prices.append(price)

    return prices


@app.task
def generate_yml_file():

    groups = Group.objects.all().order_by('id')
    attr_names = ['Тип часов', 'Цвет']
    gender_values = Value.objects.filter(attribute__name__in=attr_names)

    values_l_2 = Value.objects.filter(
        value_enum__in=[
            'Кварцевые',
            'Механические',
            'Спортивный',
            'цифровой (электронный)'
        ]
    )

    root_nodes = Node.objects.filter(_depth=1, attribute_values__in=gender_values)
    nodes_l_2 = Node.objects.filter(parent__in=root_nodes, _depth=2, attribute_values__in=values_l_2)
    country_values = Value.objects.filter(attribute__name='Страна')
    parent_nodes = nodes_l_2.union(root_nodes)
    parents = [parent for parent in parent_nodes]
    nodes_l_3 = Node.objects.filter(parent__in=parents).filter(attribute_values__in=country_values)

    nodes = root_nodes.union(nodes_l_2)
    nodes = nodes.union(nodes_l_3)
    nodes = [node.id for node in nodes]
    root = Node.objects.get(_depth=0)
    nodes.append(root.id)
    qs = Node.objects.filter(id__in=nodes).exclude(name__contains='Swiss Military')
    nodes = list(qs)
    nodes.sort(key=sorting_function)

    for category in Node.objects.all():
        cat_av = category.attribute_values.all()
        cat_av_set = {v.id for v in cat_av}

        for node in nodes:
            node_av = node.attribute_values.all()
            node_av_set = {v.id for v in node_av}
            difference = node_av_set.difference(cat_av_set)
            if len(difference) == 0 and node._depth != 0:
                category.add_rr_node(node)
                
    category = Node.objects.get(_depth=0)
    category.add_rr_node(category)

    products = Product.objects.available()
    date = now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M')

    context = {
        'base_url': 'https://presidentwatches.ru', 
        'date': date,
        'categories': nodes,
        'qs': qs,
        'products': products,
        'get_nodes_by_product': lambda qs, product: get_nodes_by_product(qs, product),
        'club_prices': lambda instance: club_prices(groups=groups, instance=instance)
    }

    xml_raw = render_to_string(
        template_name="api/retail-rocket.xml",
        context=context
    )

    with open(FILEPATH, "w") as fp:
        fp.write(xml_raw)


@app.task
def update_images():
    for instance in Product.objects.all():
        
        try:
            image = instance.image.url
            thumb = instance.thumbnail.url
        except OSError:
            instance.image = instance.image.field.default
            instance.save()
            instance.image.close()
            instance.thumbnail.close()


app.add_periodic_task(
    crontab(minute="01", hour='05'),
    generate_yml_file.s(),
    name='generate_yml_file',
)
