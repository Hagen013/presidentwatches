
"""
Settening for tests
"""

from .local import *

DEBUG = True

INSTALLED_APPS.append('core.tests')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('backend/db.sqlite3')),
    }
}

MEDIA_ROOT = str(ROOT_DIR.path('TEST_MEDIA_ROOT/'))
