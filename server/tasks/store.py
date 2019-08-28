import requests

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.conf import settings

from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from shop.models import ProductPage as Product


API_URL = settings.STORE_API_URL
LOGIN = settings.STORE_LOGIN
PASSWORD = settings.STORE_PASSWORD
STORE_ID = settings.STORE_ID

@app.task
def sync_store():
    models_in_store = set()
    with requests.Session() as session:
        session.auth = (LOGIN, PASSWORD)
        limit = 100
        params = {
            'offset': 0,
            'limit': limit,
            'store.id': STORE_ID,
        }
        page_num = 0
        while True:
            resp = session.get(API_URL, params=params)
            rows = resp.json()['rows']
            if not rows:
                break
            for row in rows:
                quantity = int(row['quantity'])
                if quantity <= 0:
                    continue
                upid = row.get('article', None)
                if upid is not None:
                    models_in_store.add(upid)
            page_num += 1
            params['offset'] = page_num * limit
            time.sleep(0.25)  # Не более 5 запросов в секунду с одного адреса от одного пользователя
        
        Product.objects.update(is_in_store=False)
        Product.objects.filter(model__in=models_in_store).update(is_in_store=True)


app.add_periodic_task(
    crontab(minute=0,  hour='*/2'),
    sync_store.s(),
    name='sync_store',
)