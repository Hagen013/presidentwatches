from .base import *

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


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


# SESSIONS SETTINGS START
SESSION_ENGINE = 'core.sessions'
SESSION_COOKIE_AGE = 60
# SESSIONS SETTINGS END


# MEDIA FILES CONFIGURATION START
# ------------------------------------------------------------------------------
MEDIA_ROOT = "/var/president_media/presidentwatches-original/"
MEDIA_URL = '/media/'
STATIC_ROOT = str(ROOT_DIR.path('client/static_production'))
ADMIN_UPLOADS = MEDIA_ROOT + 'admin/uploads/'
ADMIN_DOWNLOADS = MEDIA_ROOT + 'admin/downloads/'
# MEDIA FILES CONFIGURATION END
# ------------------------------------------------------------------------------


# YML INTEGRATIONS START
# ------------------------------------------------------------------------------
YML_PATH = MEDIA_ROOT + "yml/"
# ------------------------------------------------------------------------------
# YML LOCATION API END


# GEO LOCATION API START
# ------------------------------------------------------------------------------
GEO_LOCATION_HOST = 'geo'
GEO_LOCATION_PORT = 8282
GEO_LOCATION_SERVICE_URL = 'http://{host}:{port}/'.format(
    host=GEO_LOCATION_HOST,
    port=GEO_LOCATION_PORT
)
DEFAULT_KLADR_CODE = '7700000000000'
# ------------------------------------------------------------------------------
# GEO LOCATION API END


# SENTRY START
# ------------------------------------------------------------------------------
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://7b8a8da341734e08a5a80110a048ad6b@sentry.io/1529685",
    integrations=[DjangoIntegration()]
)
# ------------------------------------------------------------------------------
# SENTRY END