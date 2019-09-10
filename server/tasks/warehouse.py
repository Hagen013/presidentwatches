import os

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import pandas as pd
import numpy as np
from transliterate import translit

from config.celery import app
from shop.models import ProductPage as Product
from shop.models import AttributeValue as Value
from shop.models import Attribute


@app.task
def generate_warehouse_file(filepath):
    fields = [
        'brand',
        'model',
        'is_published',
        '_price',
        '_purchase_price',
        'old_price',
        'is_sale',
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
    df['is_sale'] = df['is_sale'].apply(int)
    df['is_new'] = df['is_new'].apply(int)
    df['is_bestseller'] = df['is_bestseller'].apply(int)
    df['is_yml_offer'] = df['is_yml_offer'].apply(int)
    df['is_published'] = df['is_published'].apply(int)
    df = df.reindex(fields, axis=1)
    df = df.rename(columns={
        'brand': 'Бренд',
        'model': 'Модель',
        'is_published': 'Опубликовано',
        '_price': 'Цена',
        '_purchase_price': 'Оптовая цена',
        'old_price': 'Цена до скидки',
        'is_sale': 'Распродажа',
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
        'sales_changed': 0,
        'sales_changed2true': 0,
        'sales_changed2false': 0,
        'bestseller_changed': 0,
        'new_changed': 0,
        'series_changed': 0,
        'brands_changed': 0,
        'published_changed': 0,
        'yml_changed': 0
    }

    with transaction.atomic():

        sale_value = Value.objects.get(
            attribute__name='Распродажа',
            value_bool=True
        )

        brand_attr = Attribute.objects.get(
            name='Бренд'
        )

        series_attr = Attribute.objects.get(
            name='Коллекция'
        )

        for index, row in df.iterrows():

            model = row['Модель']
            price = int(row['Цена'])
            base_price = row['Оптовая цена']
            old_price = row['Цена до скидки']
            if np.isnan(base_price):
                base_price = 0

            if np.isnan(old_price):
                old_price = 0
            else:
                old_price = int(old_price)

            is_in_stock = bool(row['В наличии'])
            is_bestseller = bool(row['Бестселлер'])
            is_new = bool(row['Новинка'])
            is_yml = bool(row['YML'])
            series = row['Коллекция']
            brand = row['Бренд']
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

                instance.old_price = old_price

                if instance._price != price:
                    instance._price = price
                    report['price_changed'] += 1
                    has_changed = True

                if instance._purchase_price != base_price:
                    instance._purchase_price = base_price
                    report['base_price_changed'] += 1
                    has_changed = True


                if instance.old_price > instance._price:
                    
                    if instance.is_sale:
                        percentage = instance.sale_percentage
                        instance.add_value(sale_value)
                        instance.caclculate_sale_percentage()
                        if percentage != instance.sale_percentage:
                            report['sales_changed'] += 1
                            has_changed = True
                    else:
                        instance.is_sale = True
                        instance.add_value(sale_value)
                        instance.caclculate_sale_percentage()
                        report['sales_changed'] += 1
                        report['sales_changed2true'] += 1
                        has_changed = True

                if instance.old_price < instance._price:

                    if instance.is_sale:
                        instance.is_sale = False
                        instance.remove_value(sale_value)
                        report['sales_changed'] += 1
                        report['sales_changed2false'] += 1
                        has_changed = True
                    else:
                        pass

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

                ## БРЕНДЫ И КОЛЛЕКЦИЯ
                if str(series) != 'nan' and str(series) != '':
                        
                    if instance.series != series:
                        instance.series = series
                        report['series_changed'] += 1
                        has_changed = True

                        if instance.series_value is None:
                            new_value = Value.objects.get_or_create(
                                attribute=series_attr,
                                value=series
                            )
                            instance.add_value(new_value)
                        elif instance.series != series:
                            new_value = Value.objects.get_or_create(
                                attribute=series_attr,
                                value=series
                            )
                            instance.add_value(new_value)

                if str(brand) != 'nan' and str(brand) != '':

                    if instance.brand != brand :
                        instance.brand = brand
                        report['brands_changed'] += 1
                        has_changed = True

                        if instance.brand_value is None:
                            new_value = Value.objects.get_or_create(
                                attribute=brand_attr,
                                value=brand
                            )
                            instance.add_value(new_value)
                        elif instance.brand_value.value != brand:
                            instance.remove_value(instance.brand_value) 
                            new_value = Value.objects.get_or_create(
                                attribute=brand_attr,
                                value=brand
                            )
                            instance.add_value(new_value)

                ## БРЕНДЫ И КОЛЛЕКЦИЯ КОНЕЦ

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
            {'label': 'Брендов:', 'quantity': report['brands_changed']},
            {'label': 'Опубликованных:', 'quantity': report['published_changed']},
            {'label': 'YML товаров:', 'quantity': report['yml_changed']},
            {'label': 'Скидок:', 'quantity': report['sales_changed']},
            {'label': 'Добавлено скидок:', 'quantity': report['sales_changed2true']},
            {'label': 'Убрано скидок:', 'quantity': report['sales_changed2false']},
        ]
    }

            
@app.task
def process_warehouse_file_2(path):

    df = pd.read_excel(path)

    report = {
        'changed': 0,
        'not_found': 0,
        'brands_changed': 0,
        'published_changed': 0,
        'published_changed2true': 0,
        'published_changed2false': 0,
        'price_changed': 0,
        'base_price_changed': 0,
        'sales_changed': 0,
        'sales_changed2true': 0,
        'sales_changed2false': 0,
        'purchase_price_changed': 0,
        'availability_changed': 0,
        'availability_changed2false': 0,
        'availability_changed2true': 0,
        'new_changed': 0,
        'new_changed2false': 0,
        'new_changed2true': 0,
        'bestseller_changed': 0,
        'bestseller_changed2false': 0,
        'bestseller_changed2true': 0,
        'yml_changed': 0,
        'yml_changed2true': 0,
        'yml_changed2false': 0
    }

    with transaction.atomic():

        sale_value = Value.objects.get(
            attribute__name='Распродажа',
            value_bool=True
        )

        brand_attr = Attribute.objects.get(
            name='Бренд'
        )

        series_attr = Attribute.objects.get(
            name='Коллекция'
        )

        for index, row in df.iterrows():
            model = row['Модель']
            price = int(row['Цена'])
            base_price = row['Оптовая цена']
            old_price = row['Цена до скидки']
            slug = row['slug']
            if np.isnan(base_price):
                base_price = 0

            if np.isnan(old_price):
                old_price = 0
            else:
                old_price = int(old_price)

            is_in_stock = bool(row['В наличии'])
            is_bestseller = bool(row['Бестселлер'])
            is_new = bool(row['Новинка'])
            is_yml = bool(row['YML'])
            brand = row['Бренд']
            is_published = bool(row['Опубликовано'])

            try:
                instance = Product.objects.get(
                    slug=slug
                )
            except ObjectDoesNotExist:
                report['not_found'] += 1
                instance = None

            if instance is not None:

                has_changed = False

                ## БРЕНДЫ И КОЛЛЕКЦИЯ
                if str(brand) != 'nan' and str(brand) != '':

                    if instance.brand != brand :
                        instance.brand = brand
                        report['brands_changed'] += 1
                        has_changed = True

                        if instance.brand_value is None:
                            new_value = Value.objects.get_or_create(
                                attribute=brand_attr,
                                value=brand
                            )
                            instance.add_value(new_value)
                        elif instance.brand_value.value != brand:
                            instance.remove_value(instance.brand_value) 
                            new_value = Value.objects.get_or_create(
                                attribute=brand_attr,
                                value=brand
                            )
                            instance.add_value(new_value)
                ## БРЕНДЫ И КОЛЛЕКЦИЯ КОНЕЦ

                if instance._price != price:
                    instance._price = price
                    report['price_changed'] += 1
                    has_changed = True

                if instance._purchase_price != base_price:
                    instance._purchase_price = base_price
                    report['base_price_changed'] += 1
                    has_changed = True


                if instance.old_price > instance._price:
                    
                    if instance.is_sale:
                        percentage = instance.sale_percentage
                        instance.add_value(sale_value)
                        instance.caclculate_sale_percentage()
                        if percentage != instance.sale_percentage:
                            report['sales_changed'] += 1
                            has_changed = True
                    else:
                        instance.is_sale = True
                        instance.add_value(sale_value)
                        instance.caclculate_sale_percentage()
                        report['sales_changed'] += 1
                        report['sales_changed2true'] += 1
                        has_changed = True

                if instance.old_price < instance._price:

                    if instance.is_sale:
                        instance.is_sale = False
                        instance.remove_value(sale_value)
                        report['sales_changed'] += 1
                        report['sales_changed2false'] += 1
                        has_changed = True
                    else:
                        pass

                if instance.is_published != is_published:
                    instance.is_published = is_published
                    report['published_changed'] += 1
                    has_changed = True

                if instance.is_yml_offer != is_yml:
                    instance.is_yml_offer = is_yml
                    report['yml_changed'] += 1
                    has_changed = True

                if instance.is_bestseller != is_bestseller:
                    instance.is_bestseller = is_bestseller
                    report['bestseller_changed'] += 1
                    has_changed = True

                if instance.is_new != is_new:
                    instance.is_new = is_new
                    report['new_changed'] += 1
                    has_changed = True

                if instance.is_in_stock != is_in_stock:
                    instance.is_in_stock = is_in_stock
                    report['availability_changed'] += 1
                    has_changed = True

                    if is_in_stock == True:
                        report['availability_changed2true'] += 1
                    else:
                        report['availability_changed2false'] += 1

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
            {'label': 'На "в налиичии":', 'quantity': report['availability_changed2true']},
            {'label': 'На "не в наличии":', 'quantity': report['availability_changed2false']},
            {'label': 'Бестселлеров:', 'quantity': report['bestseller_changed']},
            {'label': 'Новинок:', 'quantity': report['new_changed']},
            {'label': 'Брендов:', 'quantity': report['brands_changed']},
            {'label': 'Опубликованных:', 'quantity': report['published_changed']},
            {'label': 'YML товаров:', 'quantity': report['yml_changed']},
            {'label': 'Скидок:', 'quantity': report['sales_changed']},
            {'label': 'Добавлено скидок:', 'quantity': report['sales_changed2true']},
            {'label': 'Убрано скидок:', 'quantity': report['sales_changed2false']},
        ]
    }


@app.task
def create_product_list_from_file(filepath):

    df = pd.read_excel(filepath)
    
    count = 0
    errors = []

    with transaction.atomic():
        
        for index, row in df.iterrows():

            brand = row['Бренд']
            model = row['Модель']
            is_published = bool(row['Опубликовано'])
            price = int(row['Цена'])
            purhcase_price = int(row['Оптовая цена'])
            old_price = int(row['Цена до скидки'])
            is_sale = bool(row['Распродажа'])
            is_new = bool(row['Новинка'])
            is_bestseller = bool('Бестселлер')
            series = row['Коллекция']

            slug_body = '{brand}-{model}'.format(
                brand=brand,
                model=model,
            )
            slug = slugify(translit(slug_body, 'ru', reversed=True))

            instance = Product(
                _price=price,
                brand=brand,
                series=series,
                old_price=old_price,
                is_sale=is_sale,
                is_new=is_new,
                is_bestseller=is_bestseller,
                _purchase_price=purhcase_price,
                is_published=is_published,
                model=model,
                slug=slug,
            )
            
            try:
                instance.full_clean()
                instance.save()
                count += 1
            except Exception as e:
                msg = 'Ошибка для товарной позиции. Модель: {model}'.format(
                    model=model,
                )
                errors.append(msg)

    with transaction.atomic():

        for index, row in df.iterrows():

            model = row['Модель']
            
            try:
                instance = Product.objects.get(
                    model=model
                )
            except ObjectDoesNotExist:
                instance = None

            if instance is not None:

                brand = instance.brand
                series = instance.series

            try:
                brand_value = Value.objects.get(
                    attribute__name='Бренд',
                    value_enum=brand
                )
                instance.add_value(brand_value)
            except ObjectDoesNotExist:
                msg = 'Бренд: {brand_name} не существует'.format(
                    brand_name=brand
                )
                errors.append(msg)

            if str(series) != 'nan':
                try:
                    series_value = Value.objects.get(
                        attribute__name='Коллекция',
                        value_enum=series
                    )
                    instance.add_value(series_value)
                except ObjectDoesNotExist:
                    msg = 'Коллекция: {series_name} не существует'.format(
                        series_name=series
                    )
                    errors.append(msg)


    return {
        'results': {
            'count': count,
            'errors': errors
        }
    }