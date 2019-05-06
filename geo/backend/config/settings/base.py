import os
import environ

env = environ.Env()
env.read_env()

# PATHS
# ------------------------------------------------------------------------------
ROOT_DIR = environ.Path(__file__) - 4  # (web/backend/config/settings/base.py - 4 = web/)

# PATHS END


# SECURITY SETINGS
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')

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
]
THIRD_PARTY_APPS = [
    'django_extensions',
    'mptt',
    'rest_framework',
    'django_redis',
    'corsheaders',
    'raven.contrib.django.raven_compat',
]

LOCAL_APPS = [
    'delivery',
    'geo_ip',
    'kladr',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# APPLICATIONS CONFIGURATION END

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'config.urls'

# LOADERS CONFIGURATION
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
            ],
        },
    },
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     'DIRS': [
    #         '../frontend/templates/',
    #     ],
    #     'OPTIONS': {
    #         'environment': 'config.jinja2env.environment',
    #     }
    # },
]


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     str(ROOT_DIR.path('frontend/static')),
# )

# REDIS SETTINGS
# ------------------------------------------------------------------------------
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_HOST = "redis"


# RABBIT SETTINGS
# ------------------------------------------------------------------------------
RABBIT_USER = env('RABBIT_USER')
RABBIT_PASS = env('RABBIT_PASS')
RABBIT_HOSTNAME = env('RABBIT_HOSTNAME')
RABBIT_VHOST = env('RABBIT_VHOST')

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


# CELERY SETTINGS
# ------------------------------------------------------------------------------
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_IMPORTS = (
    'tasks.test_task',
    'tasks.sync_sdek',
    'tasks.sync_sdek_v2',
    'tasks.sync_pick_point',
)
CELERY_REDIS_MAX_CONNECTIONS = 10
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ALWAYS_EAGER = False
CELERY_IGNORE_RESULT = False
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Moscow'


SDEK_API_USER = env('SDEK_API_USER')
SDEK_API_PASSWORD = env('SDEK_API_PASSWORD')

PICKPOINT_API_USER = env('PICKPOINT_API_USER')
PICKPOINT_API_PASSWORD = env('PICKPOINT_API_PASSWORD')
