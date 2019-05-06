import pandas as pd
import numpy as np
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError


import asyncio
import aiohttp

from config.celery import app
from kladr.models import Kladr
from delivery.models import PickPointCityList, DeliveryPickPoint

import requests


API_URL = "http://e-solution.pickpoint.ru/api/"
PSTMT_LIST_URL = API_URL + "postamatlist"
CITY_LIST_URL = API_URL + "citylist"
ZONE_LIST_URL = API_URL + "getzone"
LOGIN_URL = API_URL + "login"

API_USER = settings.PICKPOINT_API_USER
API_PASSWORD = settings.PICKPOINT_API_PASSWORD


@app.task
def sync_pick_point():
    data = requests.get(PSTMT_LIST_URL).json()
    pvz_df = pd.DataFrame(data)
    session_id = requests.post(
        LOGIN_URL,
        json={
            "Login": API_USER,
            "Password": API_PASSWORD
        }
    )
    zones_data = requests.post(
        ZONE_LIST_URL,
        json={
            "FromCity": "Москва",
            "SessionId": session_id.json()["SessionId"]
        }
    )
    zone_df = pd.DataFrame(zones_data.json()["Zones"])

    from django.core.exceptions import ValidationError
    from django.db import IntegrityError

    with transaction.atomic():
        DeliveryPickPoint.objects.all().delete()
        for _, row in pvz_df.iterrows():
            zone_found = False
            try:
                code = row["CitiId"]
                city = PickPointCityList.objects.get(city_id=code)
                try:
                    zone = zone_df[(zone_df["ToPT"] == row["Number"]) & (
                        zone_df["DeliveryMode"] == "Standard")].iloc[0]
                    zone_found = True
                    tariff_type = DeliveryPickPoint.TYPE_STANDART
                except IndexError:
                    zone = zone_df[(zone_df["ToPT"] == row["Number"]) & (
                        zone_df["DeliveryMode"] == "Priority")]
                    if zone.shape[0] > 0:
                        zone = zone.iloc[0]
                        zone_found = True
                    tariff_type = DeliveryPickPoint.TYPE_PRIORITY

                pvz_type = {
                    "ПВЗ": DeliveryPickPoint.PVZ,
                    "АПТ": DeliveryPickPoint.APT,
                }.get(row["TypeTitle"])

                if zone_found:

                    delivery_pick_point = DeliveryPickPoint(
                        kladr=city.kladr,
                        city=city,
                        name=row["Name"],
                        latitude=row["Latitude"],
                        longitude=row["Longitude"],
                        address=row["Address"],
                        description=row["InDescription"] + ";" + row["InDescription"] + ";" + row["WorkTime"],
                        code=row["Number"],
                        pvz_type=pvz_type,
                        max_box_size=row["MaxBoxSize"],
                        zone=zone["Zone"],
                        coefficient=zone["Koeff"],
                        tariff_type=tariff_type,
                        time_min=zone["DeliveryMin"],
                        time_max=zone["DeliveryMax"]
                    )
                    delivery_pick_point.full_clean()
                    delivery_pick_point.save()


            except (PickPointCityList.DoesNotExist, IntegrityError, ValidationError) as e:
                pass
                # print(e)
