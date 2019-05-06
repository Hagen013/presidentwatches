from .base import *

import raven


DEBUG = False

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

POSTGRES_DATABASE = env('POSTGRES_DATABASE')
POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
POSTGRES_HOST = env('POSTGRES_HOST')

STATIC_ROOT = str(ROOT_DIR.path('frontend/static_production'))

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

# MEDIA FILES CONFIGURATION
# ------------------------------------------------------------------------------
MEDIA_ROOT = "/var/graph_market/"
MEDIA_URL = '/media/'

ADMIN_UPLOADS = MEDIA_ROOT + 'admin/uploads/'
ADMIN_DOWNLOADS = MEDIA_ROOT + 'admin/downloads/'

LOGS_DIR = MEDIA_ROOT + 'logs/'
SEARCH_LOGS_DIR = LOGS_DIR + 'search/'

MEDIA_BUFFER_DIRNAME = 'buffer'
MEDIA_BUFFER_PATH = '{0}{1}/'.format(MEDIA_ROOT, MEDIA_BUFFER_DIRNAME)

MEDIA_STORAGE_DIRNAME = 'storage/'
MEDIA_STORAGE_PATH = '{0}{1}'.format(MEDIA_ROOT, MEDIA_STORAGE_DIRNAME)

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'


# YML UPLOADS CONFIGURATION
# ------------------------------------------------------------------------------
YML_PATH = MEDIA_ROOT + "yml/"

MYWAREHOUSE_YML_PATH = MEDIA_ROOT + "mywarehouse/"

# SENTRY SETTINGS
# ------------------------------------------------------------------------------
RAVEN_CONFIG = {
    'dsn': env('RAVEN_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}


# SENTRY SETTINGS
# ------------------------------------------------------------------------------
# RAVEN_CONFIG = {
#     'dsn': env('RAVEN_DSN'),
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
# }

# # LOGGING SETTINGS
# # ------------------------------------------------------------------------------
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'root': {
#         'level': 'WARNING',
#         'handlers': ['sentry'],
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                       '%(process)d %(thread)d %(message)s'
#         },
#     },
#     'handlers': {
#         'sentry': {
#             'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
#             'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#             'tags': {'custom-tag': 'x'},
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'raven': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'sentry.errors': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         }
#     },
# }