from .develop import *

MEDIA_ROOT = str('/var/president_media/presidentwatches-original/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geo',
        'USER': 'geo_admin',
        'PASSWORD': '1234qwer',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Delivery
SDEK_LOGIN = '715fb13e913b10d153dcf7340559e1bf'
SDEK_PASSWORD = 'd3cd013d6a6edd389fb552faa2538087'

PICKPOINT_LOGIN = 'r4JQm0'
PICKPOINT_PASSWORD = 'uQVq8GD71IW'

