from .base import *

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
