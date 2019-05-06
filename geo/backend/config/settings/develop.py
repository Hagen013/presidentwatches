from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('backend/db.sqlite3')),
    }
}


MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1']

MEDIA_ROOT = str(ROOT_DIR.path('MEDIA_ROOT_CUBES/'))

STATIC_URL = '/static/'
MEDIA_URL = '/media/'