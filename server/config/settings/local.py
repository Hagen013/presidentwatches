from .develop import *


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
