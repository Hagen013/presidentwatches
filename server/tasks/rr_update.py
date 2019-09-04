from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings

from config.celery import app

from shop.models import Attribute
from shop.models import CategoryPage as Node
from shop.models import ProductPage as Product
from shop.models import AttributeValue as Value

def sorting_function(node):
    try:
        order = node.attribute_values.last().attribute.order
    except AttributeError:
        order = 0
    return (node._depth, order)

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


japanese = Node.objects.get(name='Японские наручные часы')
swiss = Node.objects.get(name='Швейцарские часы')
american = Node.objects.get(name='Американские наручные часы')
german = Node.objects.get(name='Немецкие наручные часы')
fashion = Node.objects.get(name='Fashion часы')
other = Node.objects.get(name='Другие часы')
electro = Node.objects.get(name='Электронные часы')

quarz = Node.objects.get(name='Кварцевые часы')
mech = Node.objects.get(name='Мужские часы')


node_1 = Node.objects.get(name='Женские японские часы')
node_2 = Node.objects.get(name='Мужские японские часы')
japanese.add_rr_node(node_1)
japanese.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские швейцарские наручные часы')
node_2 = Node.objects.get(name='Мужские швейцарские наручные часы')
swiss.add_rr_node(node_1)
swiss.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские американские часы')
node_2 = Node.objects.get(name='Мужские швейцарские наручные часы')
american.add_rr_node(node_1)
american.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские немецкие часы')
node_2 = Node.objects.get(name='Мужские немецкие часы')
german.add_rr_node(node_1)
german.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские fashion часы')
node_2 = Node.objects.get(name='Мужские fashion часы')
fashion.add_rr_node(node_1)
fashion.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские часы прочих производителей')
node_2 = Node.objects.get(name='Мужские часы прочих производителей')
other.add_rr_node(node_1)
other.add_rr_node(node_2)

node_1 = Node.objects.get(name='Кварцевые женские часы')
node_2 = Node.objects.get(name='Кварцевые мужские часы')
quarz.add_rr_node(node_1)
quarz.add_rr_node(node_2)

node_1 = Node.objects.get(name='Электронные женские часы')
node_2 = Node.objects.get(name='Мужские электронные часы')
electro.add_rr_node(node_1)
electro.add_rr_node(node_2)

node_1 = Node.objects.get(name='Женские механические часы')
node_2 = Node.objects.get(name='Механические мужские часы')
mech.add_rr_node(node_1)
mech.add_rr_node(node_2)