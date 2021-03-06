import locale
locale.setlocale(locale.LC_ALL, '')

import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from urllib.parse import urlencode

from jinja2 import Environment
from jinja2 import nodes
from jinja2.ext import Extension

from cart.last_seen import LastSeenController
from cart.cart import Cart
from geo.locations import locations

from .jinja2htmlcompress import HTMLCompress


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


def price_filter(value):
    if value is not None:
        if (value > 0):
            return 'За <span class="price">{price}</span>'.format(price=int(value))
        else:
            return 'Бесплатно'
    else:
        return ''

def time_filter(time_min, time_max):
    if time_min is not None or time_max is not None:
        if time_min != time_max:
            if time_min is None:
                from_time = ''
            else:
                from_time = 'от {days}'.format(days=time_min)
            if time_max is None:
                to_time = ''
            else:
                if time_min == 0 and time_max == 1:
                    return 'сегодня-завтра'
                to_time = ' до {days} дней'.format(days=time_max)
            return '{0}{1}'.format(
                from_time,
                to_time
            )
        else:
            if (time_min == 1):
                return 'от 1 дня'
            else:
                return 'от {0} дней'.format(time_min)
    else:
        return ''


PHONE_MAP = {
    'Краснодар': {'number': '+79612033485', 'public': '+7 961 203 34 85'},
    'Москва': {'number': '+74951332056', 'public': '+7 495 133 20 56'},
    'Екатеринбург': {'number': '+73433180428', 'public': '+7 343 318 04 28'},
    'Новосибирск': {'number': '+73832804229', 'public': '+7 383 280 42 29'},
    'Санкт-Петербург': {'number': '+78122004986', 'public': '+7 812 200 49 86'},
    'Нижний Новгород': {'number': '+78312119716', 'public': '+7 831 211 97 16'},
}


def city_phone(city_name):
    return PHONE_MAP.get(city_name, {'number': '+74951332056', 'public': '+7 495 133 20 56'})


def environment(**options):
    options['extensions'] = ['config.jinja2htmlcompress.SelectiveHTMLCompress']
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
        'price_filter': price_filter,
        'time_filter': time_filter,
        'city_phone': city_phone
    })
    return env