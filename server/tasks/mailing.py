import time
import json
import yaml
from random import randint
import datetime

import pandas as pd
import numpy as np

from config.celery import app
from celery.schedules import crontab

from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from shop.models import ProductPage as Product
from core.mail import Mail
from users.models import UserMarketingGroup as Group

User = get_user_model()


BASE_URL = 'https://presidentwatches.ru'

def get_or_create_user(email):
    user = None
    password = None
    
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User(
            email=email,
            username=email
        )
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        
    return user, password
        
@app.task
def notify_user(user, products, password, temporary=True):
    if temporary:
        template_name = 'mail/club-price-mailing.html'
        title = 'BLACK FRIDAY Скидки до 35%!'
    else:
        title = 'Персональная Чёрная Пятница круглый год! '
        template_name = 'mail/club-price-mailing2.html'
    context = {
        'user': user,
        'password': password,
        'BASE_URL': BASE_URL,
        'products': products,
        'uuid': user.uuid
    }
    mail = Mail(
        title=title,
        template=template_name,
        recipient=user.email,
        context=context,
    )
    mail.send()
    

def get_products(brands):
    brands = yaml.load(brands)
    brands = list(map(lambda x: x.split(':'), brands))
    brands.sort(key=lambda x: int(x[1]), reverse=True)
    
    top_brands = brands[:3]
    if len(top_brands) == 3:
        top_brands = list(map(lambda x: x[0], top_brands))
        qs = Product.objects.filter(brand__in=top_brands)[:3]
        
    else:
        qs = Product.objects.filter(is_in_stock=True, is_bestseller=True).order_by('-scoring')[:3]
        
    return qs


@app.task
def ultima_machina(filename):
    
    df = pd.read_excel(filename)
    df['Регион (КЛАДР)'] = df['Регион (КЛАДР)'].apply(str)
    timezones = pd.read_excel('Timezones.xlsx')
    
    tz = {}

    for index, row in timezones.iterrows():
        code = str(row['Kladr'])
        if len(code) < 2:
            code = '0' + code
        tz[code] = row['Time'].replace('UTC+', '').replace(':', '')[:-2]
    
    errors_filename = 'errors.txt'
    mailed_filename = 'mailed.txt'
    
    mailed_set = set()
    
    with open(mailed_filename, 'r') as fp:
        for line in fp:
            mailed_set.add(line[:-1])
    
    dt = datetime.datetime.now()
    hour = dt.hour
    
    selected_zones = set()
    
    for key, value in tz.items():
        zone_time = int(value) + hour
        if (zone_time > 15) and (zone_time < 17):
            selected_zones.add(key)
            
    df_total = None

    for code in selected_zones:
        code = str(code)
        df_slice = df[df['Регион (КЛАДР)'].str.startswith(code)]
        if df_total is None:
            df_total = df_slice
        else:
            df_total = df_total.append(df_slice, ignore_index=True)
            
    if df_total is not None:
        
        df_total = df_total[~df_total['Email'].isin(mailed_set)]
        
        for index, row in df_total.iterrows():
            email = row['Email']
            orders_count = row['Число заказов']
            total = row['total_sum']
            brands = row['Бренды']
            
            user, password = get_or_create_user(email)
            products = get_products(brands)
            
            if orders_count >= 3 and total >= 30000:
                try:
                    print(email)
                    notify_user(user, products, password, temporary=False)
                    with open(mailed_filename, 'a') as fp:
                        fp.write(email+'\n')
                except:
                    with open('errors.txt', 'a') as fp:
                        fp.write(email+'\n')
            else:
                try:
                    print(email)
                    notify_user(user, products, password, temporary=True)
                    with open(mailed_filename, 'a') as fp:
                        fp.write(email+'\n')
                except:
                    with open('errors.txt', 'a') as fp:
                        fp.write(email+'\n')