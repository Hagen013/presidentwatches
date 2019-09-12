'''
Базовые настройки
'''

import os
import environ
from datetime import timedelta
from kombu import Queue, Exchange


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
    'reviews',
    'geo',
    'info',
    'payments',
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
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
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
    'x-token',
    'Bearer'
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


# ELASTICSEARCH SETTINGS START
# ------------------------------------------------------------------------------
ELASTICSEARCH_HOST = 'elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_URL = 'http://{0}:{1}/'.format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
ELASTICSEARCH_SNAPSHOT_REPO = 'backups'
ELASTICSEARCH_SNAPSHOT_NAME = 'backup'
ELASTICSEARCH_SNAPSHOT_DIR = '/var/graph_market/elastic-snapshots/'
#-------------------------------------------------------------------------------
# ELASTICSEARCH SETTINGS END


# GEO LOCATION API START
# ------------------------------------------------------------------------------
GEO_LOCATION_HOST = 'localhost'
GEO_LOCATION_PORT = 8282
GEO_LOCATION_SERVICE_URL = 'http://{host}:{port}/'.format(
    host=GEO_LOCATION_HOST,
    port=GEO_LOCATION_PORT
)
DEFAULT_KLADR_CODE = '7700000000000'
# ------------------------------------------------------------------------------
# GEO LOCATION API END


# CUSTOM AUTH START
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'
# ------------------------------------------------------------------------------
# CUSTOM AUTH END


# SIMPLE_JWT START
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}
# ------------------------------------------------------------------------------
# SIMPLE_JWT END


# REDIS SETTINGS START
# ------------------------------------------------------------------------------
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = 'redis'
# ------------------------------------------------------------------------------
# REDIS SETTINGS END


# RABBIT SETTINGS START
# ------------------------------------------------------------------------------
RABBIT_HOSTNAME = 'rabbit'
RABBIT_USER = os.environ.get('RABBIT_USER', 'RABBIT_USER')
RABBIT_PASS = os.environ.get('RABBIT_PASS', 'RABBIT_PASS')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST', 'RABBIT_VHOST')

BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=RABBIT_USER,
    password=RABBIT_PASS,
    hostname=RABBIT_HOSTNAME,
    vhost=RABBIT_VHOST,
)
# We don't want to have dead connections stored on rabbitmq,
# so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'

if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT
BROKER_POOL_LIMIT = 10
BROKER_CONNECTION_TIMEOUT = 10
# ------------------------------------------------------------------------------
# RABBIT SETTINGS END


# CELERY SETTINGS START
# ------------------------------------------------------------------------------
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_IMPORTS = (
    'tasks.warehouse',
    'tasks.elastic',
    'tasks.sms_notifications',
    'tasks.retail_rocket',
    'tasks.yml',
    'tasks.store'
)
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('media', Exchange('media'), routing_key='media')
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_ROUTES = {
}
CELERY_REDIS_MAX_CONNECTIONS = 8
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ALWAYS_EAGER = False
CELERY_IGNORE_RESULT = False
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/Moscow'
# ------------------------------------------------------------------------------
# CELERY SETTINGS END


# SMS MESSAGES START
# ------------------------------------------------------------------------------
SMS_URL = env("DJANGO_SMS_URL")
SMS_SECRET_KEY = env("DJANGO_SMS_SECRET_KEY")
# ------------------------------------------------------------------------------
# SMS MESSAGES END


# STORE START
# ------------------------------------------------------------------------------
STORE_LOGIN = env('DJANGO_STORE_LOGIN')
STORE_PASSWORD = env('DJANGO_STORE_PASSWORD')
STORE_ID = env('DJANGO_STORE_ID')
STORE_API_URL = env('DJANGO_STORE_URL')
# ------------------------------------------------------------------------------
# STORE END


# YANDEX KASSA START
YANDEX_KASSA_API = env('YANDEX_KASSA_API')
YANDEX_KASSA_SHOP_ID = env('YANDEX_KASSA_SHOP_ID')
YANDEX_KASSA_SECRET = env('YANDEX_KASSA_SECRET')
# YANDEX KASSA END