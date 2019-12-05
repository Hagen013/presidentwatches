import requests
import time

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
                upid = row.get('code', None)
                print(upid)
                if upid is not None:
                    try:
                        upid = int(upid)
                        models_in_store.add(upid)
                    except ValueError:
                        pass
            page_num += 1
            params['offset'] = page_num * limit
            time.sleep(0.25)  # Не более 5 запросов в секунду с одного адреса от одного пользователя
        
        Product.objects.update(is_in_store=False)
        qs = Product.objects.filter(id__in=models_in_store)
        print('###')
        print(qs.count())
        print('###')
        qs.update(is_in_store=True)


app.add_periodic_task(
    crontab(minute=0,  hour='*/2'),
    sync_store.s(),
    name='sync_store',
)