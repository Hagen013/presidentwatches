import locale
locale.setlocale(locale.LC_ALL, '')

import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from urllib.parse import urlencode

from jinja2 import Environment

from cart.last_seen import LastSeenController
from cart.cart import Cart
from geo.locations import locations


NOUN_MAPPING_MASCULINE = {
    '1': '',
    '2': 'а',
    '3': 'а',
    '4': 'а',
    '5': 'ов',  
}

NOUN_MAPPING_FEMININE = {
    '1': 'а',
    '2': 'ы',
    '3': 'ы',
    '4': 'ы',
    '5': ''
}


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


def locations_list():
    return locations


def format_price(value):
    return '{:,d}'.format(value).replace(',', ' ')


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

def rating_stars(scoring):
    template = ""
    empty_positions = 5 - scoring
    for i in range(scoring):
        template += '<div class="star star_full"></div>'
    for i in range(empty_positions):
        template += '<div class="star star_hollow"></div>'
    return template


def ratings_stars_float(scoring):
    template = ""
    rounded = round(scoring)
    empty_positions = 5 - rounded
    for i in range(rounded):
        template += '<div class="icon icon_star-full"></div>'
    for i in range(empty_positions):
        template += '<div class="icon icon_star-stroke"></div>'
    return template


def normalize_noun_masculine(value, noun):
    if value < 21:
        value=str(value)
        ending = NOUN_MAPPING_MASCULINE.get(value, 'ов')
        return noun + ending
    elif value < 101:
        value = str(value)[1:]
        ending = NOUN_MAPPING_MASCULINE.get(value, 'ов')
        return noun + ending
    else:
        value = str(value)[2:]
        ending = NOUN_MAPPING_MASCULINE.get(value, 'ов')
        return noun + ending


def normalize_noun_feminine(value, noun):
    if value < 21:
        value=str(value)
        ending = NOUN_MAPPING_FEMININE.get(value, '')
        return noun + ending
    elif value < 101:
        value = str(value)[1:]
        ending = NOUN_MAPPING_FEMININE.get(value, '')
        return noun + ending
    else:
        value = str(value)[2:]
        ending = NOUN_MAPPING_FEMININE.get(value, '')
        return noun + ending


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'last_seen': last_seen,
        'update_pagination': update_pagination,
        'sorting_option_class': sorting_option_class,
        'session_cart': session_cart,
        'locations_list': locations_list,
        'format_price': format_price,
        'rating_stars': rating_stars,
        'ratings_stars_float': ratings_stars_float,
        'normalize_noun_masculine': normalize_noun_masculine,
        'normalize_noun_feminine': normalize_noun_feminine,
    })
    return env