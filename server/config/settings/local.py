from .develop import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('server/db.sqlite3')),
    }
}

# MEDIA FILES CONFIGURATION START
# ------------------------------------------------------------------------------
MEDIA_ROOT = "/var/test/"
MEDIA_URL = '/media/'
# MEDIA FILES CONFIGURATION END
# ------------------------------------------------------------------------------
