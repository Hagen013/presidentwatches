import os

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import transaction

import pandas as pd
import numpy as np

from config.celery import app
from shop.models import ProductPage as Product


@app.task
def generate_warehouse_file(filepath):
    fields = [
        'brand',
        'model',
        'is_published',
        '_price',
        '_purchase_price',
        'is_in_stock',
        'is_new',
        'is_bestseller',
        'is_yml_offer',
        'slug',
        'series'
    ]
    qs = Product.objects.all().values(
        *fields
    )
    df = pd.DataFrame(list(qs))
    df['is_in_stock'] = df['is_in_stock'].apply(int)
    df = df.reindex(fields, axis=1)
    df = df.rename(columns={
        'brand': 'Бренд',
        'model': 'Модель',
        'is_published': 'Опубликовано',
        '_price': 'Цена',
        '_purchase_price': 'Оптовая цена',
        'is_in_stock': 'В наличии',
        'is_new': 'Новинка',
        'is_bestseller': 'Бестселлер',
        'is_yml_offer': 'YML',
        'slug': 'slug',
        'series': 'Коллекция'
    })
    writer = pd.ExcelWriter(filepath)
    df.to_excel(writer, 'Ostatki')
    writer.save()

    return {
        'filepath': filepath
    }


@app.task
def process_warehouse_file(path):
    
    df = pd.read_excel(path)

    report = {
        'changed': 0,
        'not_found': 0,
        'price_changed': 0,
        'base_price_changed': 0,
        'availability_changed': 0,
        'availability_changed_2true': 0,
        'availability_changed_2false': 0,
        'bestseller_changed': 0,
        'new_changed': 0,
        'series_changed': 0,
        'published_changed': 0,
        'yml_changed': 0
    }

    with transaction.atomic():
        for index, row in df.iterrows():

            model = row['Модель']
            price = int(row['Цена'])
            base_price = row['Оптовая цена']
            if np.isnan(base_price):
                base_price = 0

            is_in_stock = bool(row['В наличии'])
            is_bestseller = bool(row['Бестселлер'])
            is_new = bool(row['Новинка'])
            is_yml = bool(row['YML'])
            series = row['Коллекция']
            is_published = bool(row['Опубликовано'])

            try:
                instance = Product.objects.get(
                    model=model
                )

            except ObjectDoesNotExist:
                instance = None
                report['not_found'] += 1
            
            if instance is not None:

                has_changed = False

                if instance._price != price:
                    instance._price = price
                    report['price_changed'] += 1
                    has_changed = True

                if instance._purchase_price != base_price:
                    instance._purchase_price = base_price
                    report['base_price_changed'] += 1
                    has_changed = True

                if instance.is_in_stock != is_in_stock:
                    instance.is_in_stock = is_in_stock
                    report['availability_changed'] += 1
                    has_changed = True

                    if is_in_stock == True:
                        report['availability_changed_2true'] += 1
                    else:
                        report['availability_changed_2false'] += 1

                if instance.is_bestseller != is_bestseller:
                    instance.is_bestseller = is_bestseller
                    report['bestseller_changed'] += 1
                    has_changed = True

                if instance.is_new != is_new:
                    instance.is_new = is_new
                    report['new_changed'] += 1
                    has_changed = True

                if str(series) != 'nan' and str(series) != '':
                        
                    if instance.series != series :
                        print(series)
                        instance.series = series
                        report['series_changed'] += 1
                        has_changed = True

                if instance.is_published != is_published:
                    instance.is_published = is_published
                    report['published_changed'] += 1
                    has_changed = True

                if instance.is_yml_offer != is_yml:
                    instance.is_yml_offer = is_yml
                    report['yml_changed'] += 1
                    has_changed = True

                if has_changed:
                    instance.save()
                    report['changed'] += 1


    return {
        'not_found': report['not_found'],
        'results': [
            {'label': 'Всего:', 'quantity': report['changed']},
            {'label': 'Цен:', 'quantity': report['price_changed']},
            {'label': 'Опт. цен:', 'quantity': report['base_price_changed']},
            {'label': 'Наличие:', 'quantity': report['availability_changed']},
            {'label': 'На "в налиичии":', 'quantity': report['availability_changed_2true']},
            {'label': 'На "не в наличии":', 'quantity': report['availability_changed_2false']},
            {'label': 'Бестселлеров:', 'quantity': report['bestseller_changed']},
            {'label': 'Новинок:', 'quantity': report['new_changed']},
            {'label': 'Коллекций:', 'quantity': report['series_changed']},
            {'label': 'Опубликованных:', 'quantity': report['published_changed']},
            {'label': 'YML товаров:', 'quantity': report['yml_changed']},
        ]
    }

            




                    

