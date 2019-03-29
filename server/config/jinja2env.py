import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from urllib.parse import urlencode

from jinja2 import Environment

from cart.last_seen import LastSeenController
from cart.cart import Cart


def update_pagination(querystring, kwargs):
    query = querystring.dict()
    page = kwargs.get('page')
    if page == 1:
        kwargs.pop('page')
        query.pop('page')
    query.update(kwargs)
    if len(query.keys()) > 0:
        return "?" + urlencode(query)
    return ""


storing_mapping = {
    '_price': 'price',
    '-_price': 'price',
    '-scoring': 'scoring',
    '-scoring': 'scoring',
    '-sale_percentage': 'sale_percentage',
    'sale_percentage': 'sale_percentage',
    'created_at': 'created_at'
}

def sorting_option_class(option, active_option):
    css = ''
    mapping_value = storing_mapping.get(active_option, None)
    if mapping_value is not None:
        if mapping_value == option:
            css += 'active'
            if active_option[0] == '-':
                css += ' decrement'
    return css


def last_seen(request):
    return LastSeenController(request).data['items']

def session_cart(request):
    cart = Cart(request)
    return cart

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'last_seen': last_seen,
        'update_pagination': update_pagination,
        'sorting_option_class': sorting_option_class,
        'session_cart': session_cart
    })
    return env