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
    'delivery',
    'tasks',
    'blog',
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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            '../client/templates/',
        ],
        'OPTIONS': {
            'environment': 'config.jinja2env.environment',
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
)
# ------------------------------------------------------------------------------
# STATIC FILES END
