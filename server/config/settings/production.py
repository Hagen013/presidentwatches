from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False

STATIC_ROOT = str(ROOT_DIR.path('client/static_production'))

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


# DATABASE CONFIGURATION START
# ------------------------------------------------------------------------------
POSTGRES_DATABASE = env('DJANGO_POSTGRES_DATABASE')
POSTGRES_USER     = env('DJANGO_POSTGRES_USER')
POSTGRES_PASSWORD = env('DJANGO_POSTGRES_PASSWORD')
POSTGRES_HOST     = 'postgres'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DATABASE,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': '5432',
    }
}
# DATABASE CONFIGURATION END
# ------------------------------------------------------------------------------


# MEDIA FILES CONFIGURATION START
# ------------------------------------------------------------------------------
MEDIA_ROOT = "/1TB/presidentwatches-original/"
MEDIA_URL = '/media/'
STATIC_ROOT = str(ROOT_DIR.path('client/static_production'))
# MEDIA FILES CONFIGURATION END
# ------------------------------------------------------------------------------


# SENTRY START
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn="https://0eaf056b3f6b4f758cd68cc7de62e40e@sentry.io/1438577",
    integrations=[DjangoIntegration()]
)
# SENTRY END
# ------------------------------------------------------------------------------