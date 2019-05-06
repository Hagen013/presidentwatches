import datetime
from hashlib import md5
import time

import pandas as pd
import numpy as np
import asyncio
import aiohttp

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from config.celery import app
from delivery.models import SdekCityList


AUTH_LOGIN = settings.SDEK_API_USER
AUTH_PASSWORD = settings.SDEK_API_PASSWORD
CALCULATE_URL = "http://api.cdek.ru/calculator/calculate_price_by_json.php"

EXPRESS_LITE_SS = 10
PACKAGE_SS = 136
EXPRESS_LITE_SD = 11
PACKAGE_SD = 137


# UTILS
def get_price_column_name(tariff_id, weight):
    return {
        (EXPRESS_LITE_SD, 1): "price_sd_ex_1kg",
        (EXPRESS_LITE_SD, 2): "price_sd_ex_2kg",
        (PACKAGE_SD, 3): "price_sd_pkg_3kg",
        (PACKAGE_SD, 4): "price_sd_pkg_4kg",
        (EXPRESS_LITE_SS, 1): "price_ss_ex_1kg",
        (EXPRESS_LITE_SS, 2): "price_ss_ex_2kg",
        (PACKAGE_SS, 3): "price_ss_pkg_3kg",
        (PACKAGE_SS, 4): "price_ss_pkg_4kg"}[(tariff_id, weight)]


def get_time_min_column_name(tariff_id):
    return {
        PACKAGE_SS: "time_min_ss_pkg",
        PACKAGE_SD: "time_min_sd_pkg",
        EXPRESS_LITE_SS: "time_min_ss_ex",
        EXPRESS_LITE_SD: "time_min_sd_ex",
    }[tariff_id]


def get_time_max_column_name(tariff_id):
    return {
        PACKAGE_SS: "time_max_ss_pkg",
        PACKAGE_SD: "time_max_sd_pkg",
        EXPRESS_LITE_SS: "time_max_ss_ex",
        EXPRESS_LITE_SD: "time_max_sd_ex",
    }[tariff_id]


def sdek_req_data(tariff_id, receiver_city_id, weight):
    date_execute = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    return {
        "version": "1.0",
        "authLogin": AUTH_LOGIN,
        "secure": md5((date_execute + "&" + AUTH_PASSWORD).encode("utf-8")).hexdigest(),
        "dateExecute": date_execute,
        "senderCityId": "44",  # 44=Москва
        "receiverCityId": str(receiver_city_id),
        "tariffId": str(tariff_id),
        "goods": [{
            "weight": str(weight),  # kg
            "volume": str(0.0001 * 0.0001 * 0.0001),  # meters^3

        }],
    }


async def calculate_row(index, tariff_id, receiver_city_id, weight, session):
    req_data = sdek_req_data(tariff_id, receiver_city_id, weight)
    async with session.post(
        CALCULATE_URL,
        json=req_data,
        timeout=None,
    ) as resp:
        # print(tariff_id, weight, index)
        if resp.status == 200:
            data = await resp.json()
            #print(data)
            result = data.get("result", None)
            error = data.get("error", None)
            #print(result)
            if error is not None:
                error_code = error[0].get('code')
                if error_code == 18:
                    print(data)
            return tariff_id, weight, index, data
        else:
            return tariff_id, weight, index, None


async def caclulate_sdek(tariff_id, weight, df):
    conn = aiohttp.TCPConnector(limit=10)
    futures = []
    async with aiohttp.ClientSession(connector=conn) as session:
        for index, row in df.iterrows():
            future = asyncio.ensure_future(
                calculate_row(
                    index=index,
                    tariff_id=tariff_id,
                    receiver_city_id=row["city_id"],
                    weight=weight,
                    session=session
                )
            )
            futures.append(future)

        await asyncio.wait(futures)
    return futures


@app.task
def sync_sdek():
    df_full = pd.DataFrame(
        columns=[
            "id",
            "city_name",
            "city_id",
            "cash_on_delivery",
            "price_sd_ex_1kg",
            "price_sd_ex_2kg",
            "price_sd_pkg_3kg",
            "price_sd_pkg_4kg",
            "price_ss_ex_1kg",
            "price_ss_ex_2kg",
            "price_ss_pkg_3kg",
            "price_ss_pkg_4kg",
            "time_min_ss_pkg",
            "time_min_sd_pkg",
            "time_min_ss_ex",
            "time_min_sd_ex",
            "time_max_ss_pkg",
            "time_max_sd_pkg",
            "time_max_ss_ex",
            "time_max_sd_ex",
        ]
    )
    
    qs = SdekCityList.objects.all().order_by("pk")
    df_full["city_name"] = [x.city_name for x in qs]
    df_full["city_id"] = [x.city_id for x in qs]
    df_full["id"] = [x.pk for x in qs]
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    df_not_empty = True
    page_size = 100
    timeout = 60
    limit = 100
    offset = 0
    df_size = df_full.shape[0]
    
    while df_not_empty:

        df = df_full[offset:limit]
        if df.shape[0] == 0:
            df_not_empty = False
            break
        

        tasks = asyncio.wait([
            caclulate_sdek(EXPRESS_LITE_SD, 1, df),
            caclulate_sdek(EXPRESS_LITE_SD, 2, df),
            
            caclulate_sdek(PACKAGE_SD, 3, df),
            caclulate_sdek(PACKAGE_SD, 4, df),
            
            caclulate_sdek(EXPRESS_LITE_SS, 1, df),
            caclulate_sdek(EXPRESS_LITE_SS, 2, df),
            
            caclulate_sdek(PACKAGE_SS, 3, df),
            caclulate_sdek(PACKAGE_SS, 4, df)
        ])
        
        result, _ = loop.run_until_complete(tasks)
        new_rows = (y.result() for x in result for y in x.result())

        for row in new_rows:
            tariff_id, weight, index, data = row
            price_column = get_price_column_name(tariff_id, weight)
            df.loc[index, price_column] = data.get("result", {}).get("price", np.NaN)

            if weight in {1, 3}:
                time_min_column = get_time_min_column_name(tariff_id)
                time_max_column = get_time_max_column_name(tariff_id)
                min_time = data.get("result", {}).get("deliveryPeriodMin", np.NaN)
                max_time = data.get("result", {}).get("deliveryPeriodMax", np.NaN)
                df.loc[index, time_min_column] = min_time
                df.loc[index, time_max_column] = max_time
            if weight == 1:
                if data.get("result") and not data.get("result").get("cashOnDelivery"):
                    # Если есть результат и не указано - есть оплата при получении
                    df.loc[index, "cash_on_delivery"] = True
                else:
                    # Если нет результата или указан предел то считаем что её нет
                    df.loc[index, "cash_on_delivery"] = False

            df = df.where((pd.notnull(df)), None)

        # Запись в БД
        # Обновление данных
        with transaction.atomic():
            for _, row in df.iterrows():
                sdek_city = SdekCityList.objects.get(id=row["id"])

                sdek_city.price_sd_ex_1kg = row["price_sd_ex_1kg"]
                sdek_city.price_sd_pkg_3kg = row["price_sd_pkg_3kg"]
                sdek_city.price_ss_ex_1kg = row["price_ss_ex_1kg"]
                sdek_city.price_ss_pkg_3kg = row["price_ss_pkg_3kg"]

                # Данных фрагмент возможно оптимизировать
                # За счёт пандаса
                if row["price_sd_ex_1kg"] and row["price_sd_ex_2kg"]:
                    sdek_city.price_sd_ex_additional_kg = \
                        int(row["price_sd_ex_2kg"]) - int(row["price_sd_ex_1kg"])
                else:
                    sdek_city.price_sd_ex_additional_kg = None

                if row["price_sd_pkg_3kg"] and row["price_sd_pkg_4kg"]:
                    sdek_city.price_sd_pkg_additional_kg = \
                        int(row["price_sd_pkg_4kg"]) - int(row["price_sd_pkg_3kg"])
                else:
                    sdek_city.price_sd_pkg_additional_kg = None

                if row["price_ss_ex_1kg"] and row["price_ss_ex_2kg"]:
                    sdek_city.price_ss_ex_additional_kg = \
                        int(row["price_ss_ex_2kg"]) - int(row["price_ss_ex_1kg"])
                else:
                    sdek_city.price_ss_ex_additional_kg = None

                if row["price_ss_pkg_3kg"] and row["price_ss_pkg_4kg"]:
                    sdek_city.price_ss_pkg_additional_kg = \
                        int(row["price_ss_pkg_4kg"]) - int(row["price_ss_pkg_3kg"])
                else:
                    sdek_city.price_ss_pkg_additional_kg = None

                sdek_city.time_min_ss_ex = row["time_min_ss_ex"]
                sdek_city.time_min_ss_pkg = row["time_min_ss_pkg"]
                sdek_city.time_min_sd_ex = row["time_min_sd_ex"]
                sdek_city.time_min_sd_pkg = row["time_min_sd_pkg"]
                sdek_city.time_max_ss_ex = row["time_max_ss_ex"]
                sdek_city.time_max_ss_pkg = row["time_max_ss_pkg"]
                sdek_city.time_max_sd_ex = row["time_max_sd_ex"]
                sdek_city.time_max_sd_pkg = row["time_max_sd_pkg"]
                sdek_city.save()
        
        print("{limit}/{size}".format(limit=limit, size=df_size))
        limit += page_size
        offset += page_size
        time.sleep(timeout)
