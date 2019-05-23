'''
Базовые настройки
'''

import os
import environ

env = environ.Env()
env.read_env()


# ROUTING
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
# ------------------------------------------------------------------------------
# ROUTING END


# PATHS
# ------------------------------------------------------------------------------
ROOT_DIR = environ.Path(__file__) - 4  # (project/server/config/settings/base.py - 4 = project/)
# ------------------------------------------------------------------------------
# PATHS END


# SECURITY SETINGS
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')
# ------------------------------------------------------------------------------
# SECURITY SETINGS END


# APPLICATIONS CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'social_django',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'mptt',
    'imagekit'
]

LOCAL_APPS = [
    'core',
    'users',
    'eav',
    'shop',
    'cart',
    'favorites',
    'delivery',
    'tasks',
    'blog',
    'search',
    'geo',
    'info',
    'api'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# ------------------------------------------------------------------------------
# APPLICATIONS CONFIGURATION END


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RequestCookiesMiddleware',
    'geo.middleware.GeoLocationMiddleware'
]
# ------------------------------------------------------------------------------
# APPLICATIONS CONFIGURATION END


# TEMPLATES CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            '../client/templates/'
        ],
        'OPTIONS': {
            'environment': 'config.jinja2env.environment',
            'context_processors': [
                'cart.context_processors.cart_processor',
                'favorites.context_processors.favorites_processor'
            ]
        }
    },
]
# ------------------------------------------------------------------------------
# TEMPLATES CONFIGURATION END


# WSGI CONFIGURATION
# ------------------------------------------------------------------------------
WSGI_APPLICATION = 'config.wsgi.application'
# ------------------------------------------------------------------------------
# WSGI CONFIGURATION END


# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# ------------------------------------------------------------------------------
# PASSWORD VALIDATION END


# INTERNATIONALIZATION START
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = False
USE_L10N = True
USE_TZ = True
# ------------------------------------------------------------------------------
# INTERNATIONALIZATION END


# REST_FRAMEWORK START
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
# ------------------------------------------------------------------------------
# REST_FRAMEWORK END


# RESPONSE HEADERS START
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-token'
)
# ------------------------------------------------------------------------------
# RESPONSE HEADERS END


# STATIC FILES START
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(ROOT_DIR.path('client/dist')),
    str(ROOT_DIR.path('admin/dist'))
)
# ------------------------------------------------------------------------------
# STATIC FILES END


# ELASTICSEARCH SETTINGS
# ------------------------------------------------------------------------------
ELASTICSEARCH_HOST = 'elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_URL = 'http://{0}:{1}/'.format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
ELASTICSEARCH_SNAPSHOT_REPO = 'backups'
ELASTICSEARCH_SNAPSHOT_NAME = 'backup'
ELASTICSEARCH_SNAPSHOT_DIR = '/var/graph_market/elastic-snapshots/'
#-------------------------------------------------------------------------------
# ELASTICSEARCH SETTINGS END


# GEO LOCATION API
# ------------------------------------------------------------------------------
GEO_LOCATION_HOST = env('GEO_LOCATION_SERVICE_HOST')
GEO_LOCATION_PORT = 8282
GEO_LOCATION_SERVICE_URL = 'http://{host}:{port}/'.format(
    host=GEO_LOCATION_HOST,
    port=GEO_LOCATION_PORT
)
# ------------------------------------------------------------------------------
# GEO LOCATION API END