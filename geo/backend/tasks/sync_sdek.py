from hashlib import md5
import datetime
import itertools
import xml.etree.ElementTree as ET

from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import pandas as pd
import numpy as np
import asyncio
import aiohttp
import requests

from config.celery import app
from kladr.models import Kladr
from delivery.models import SdekCityList, DeliverySdekPoint

from django.conf import settings


AUTH_LOGIN = settings.SDEK_API_USER
AUTH_PASSWORD = settings.SDEK_API_PASSWORD
CALCULATE_URL = "http://api.edostavka.ru/calculator/calculate_price_by_json.php"

EXPRESS_LITE_SS = 10
PAKAGE_SS = 136
EXPRESS_LITE_SD = 11
PAKAGE_SD = 137


# UTILS FUNCTIONS
def get_price_column_name(tariff_id, weight):
    return {
        (EXPRESS_LITE_SD, 1): "price_sd_ex_1kg",
        (EXPRESS_LITE_SD, 2): "price_sd_ex_2kg",
        (PAKAGE_SD, 3): "price_sd_pkg_3kg",
        (PAKAGE_SD, 4): "price_sd_pkg_4kg",
        (EXPRESS_LITE_SS, 1): "price_ss_ex_1kg",
        (EXPRESS_LITE_SS, 2): "price_ss_ex_2kg",
        (PAKAGE_SS, 3): "price_ss_pkg_3kg",
        (PAKAGE_SS, 4): "price_ss_pkg_4kg"}[(tariff_id, weight)]


def get_time_min_column_name(tariff_id):
    return {
        PAKAGE_SS: "time_min_ss_pkg",
        PAKAGE_SD: "time_min_sd_pkg",
        EXPRESS_LITE_SS: "time_min_ss_ex",
        EXPRESS_LITE_SD: "time_min_sd_ex",
    }[tariff_id]


def get_time_max_column_name(tariff_id):
    return {
        PAKAGE_SS: "time_max_ss_pkg",
        PAKAGE_SD: "time_max_sd_pkg",
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


# Расчёт для одного тарифа для одной строки для одного веса и тд.
async def calc_sdek_row(index, tariff_id, receiver_city_id, weight, session):
    req_data = sdek_req_data(tariff_id, receiver_city_id, weight)
    async with session.post(
        CALCULATE_URL,
        json=req_data,
        timeout=None,
    ) as resp:
        # print(tariff_id, weight, index)
        if resp.status == 200:
            data = await resp.json()
            return tariff_id, weight, index, data
        else:
            return tariff_id, weight, index, None


# Расчёт для одного тарифа по всем городам
async def calc_sdek_citys(tariff_id, weight, df):
    conn = aiohttp.TCPConnector(limit=100)
    futures = []
    async with aiohttp.ClientSession(connector=conn) as session:
        for i, row in df.iterrows():
            future = asyncio.ensure_future(
                calc_sdek_row(index=i,
                              tariff_id=tariff_id,
                              receiver_city_id=row["city_id"],
                              weight=weight,
                              session=session
                              )
            )
            futures.append(future)

        await asyncio.wait(futures)
    return futures


# GOD FUNCTIONS
@app.task
def sync_sdek():
    # Описание датафрейма, эдентичного по сути таблице SdekCityList
    df = pd.DataFrame(columns=["db_id",
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
                               ])

    # Перенос данных из БД в пандас
    df["city_name"] = [x.city_name for x in SdekCityList.objects.all().order_by("pk")]
    df["city_id"] = [x.city_id for x in SdekCityList.objects.all().order_by("pk")]
    df["db_id"] = [x.pk for x in SdekCityList.objects.all().order_by("pk")]

    # Очистка евентлупа и создание новго
    loop = asyncio.get_event_loop().close()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Таск считает для каждого тарифа по всем городам
    # по сути 8 тасков обёрнутых в один
    calc_sdek_citys_tasks = asyncio.wait([
        calc_sdek_citys(EXPRESS_LITE_SD, 1, df),
        calc_sdek_citys(EXPRESS_LITE_SD, 2, df),
        calc_sdek_citys(PAKAGE_SD, 3, df),
        calc_sdek_citys(PAKAGE_SD, 4, df),

        calc_sdek_citys(EXPRESS_LITE_SS, 1, df),
        calc_sdek_citys(EXPRESS_LITE_SS, 2, df),
        calc_sdek_citys(PAKAGE_SS, 3, df),
        calc_sdek_citys(PAKAGE_SS, 4, df)
    ])

    # Запуск
    result, _ = loop.run_until_complete(calc_sdek_citys_tasks)

    # Разворачивание результата
    new_rows = (y.result() for x in result for y in x.result())
    # Анализ данных и из подготовка для записи в БД
    for x in new_rows:
        tariff_id, weight, index, data = x
        price_column = get_price_column_name(tariff_id, weight)
        df.loc[index, price_column] = data.get("result", {}).get("price", np.NaN)
        # new_date_value = data.get("result", {}).get()

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
            sdek_city = SdekCityList.objects.get(id=row["db_id"])

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


PVZ_LIST_URL = "https://integration.cdek.ru/pvzlist.php"


@app.task
def sync_sdek_points():
    data = requests.get(PVZ_LIST_URL)
    pvz_list = ET.fromstring(data.text)
    with transaction.atomic():
        DeliverySdekPoint.objects.all().delete()
        for pvz in pvz_list.getchildren():
            code = pvz.get('CityCode')
            try:
                city = SdekCityList.objects.get(city_id=code)
                sdek_delivery_point = DeliverySdekPoint(
                    name=pvz.get('Name', 'ПВЗ СДЕК'),
                    kladr=city.kladr,
                    city=city,
                    latitude=pvz.get("coordY"),
                    longitude=pvz.get("coordX"),
                    address=pvz.get("Address"),
                    description=pvz.get('Note', '') + '\n' + pvz.get('Phone', ''),
                    code=pvz.get('Code')
                )
                sdek_delivery_point.full_clean()
                sdek_delivery_point.save()
            except (SdekCityList.DoesNotExist, IntegrityError, ValidationError):
                continue
