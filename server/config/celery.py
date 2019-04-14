import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
app = Celery('graph_market')
app.config_from_object('django.conf:settings')
