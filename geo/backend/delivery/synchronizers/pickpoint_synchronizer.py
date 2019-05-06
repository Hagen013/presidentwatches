from .base_synchronizer import BaseSynchronizer
from ..models import Delivery, PickPointCityList
from kladr.models import Kladr
import requests
import json
from functools import lru_cache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings


def calculate_price(zone_num, coeff):
    # Формула для расчета = (базовая цена + тариф зоны * вес отправления) * коэффициент  *1,18
    # базовую цену принимаем равной 200 рублям
    # вес отправления 1 кг
    # на 1,18 умножаем в любом случае, так как все тарифы без НДС
    # тариф зоны указаны в приложении 2 на странице 12 (например, для зоны 3 он равен 34,2 рубля)
    # коэффициент - для областного центра 1, для необластного центра 1,25
    # окрулять тариф до следующих за числом десятков ( 231 рубль округляем
    # до 240 рублей)
    try:
        zone_tariff = {
            -1: 0.0,
            0: 8.0,
            1: 11.7,
            2: 19.5,
            3: 34.2,
            4: 46.8,
            5: 87.1,
            6: 162.0,
            7: 185.0,
            8: 270.0,
        }[zone_num]
        price = 200.0 + zone_tariff * 1
        price *= 1.18
        price = int(price / 10 + 0.99) * 10
        return price
    except:
        return None


class PickpointSynchronizer(BaseSynchronizer):
    queryset = Delivery.objects.filter(delivery_type=Delivery.PICK_POINT)
    delivery_type = Delivery.PICK_POINT

    API_URL = "http://e-solution.pickpoint.ru/api/"
    PSTMT_LIST_URL = API_URL + "postamatlist"
    ZONE_LIST_URL = API_URL + "getzone"

    API_USER = settings.PICKPOINT_LOGIN
    API_PASSWORD = settings.PICKPOINT_PASSWORD

    KLADR_PICKPOINT_MAP = {
        'Октябрьский (Люберецкий)': 'Октябрьский',
        'Одинцово (Одинцовский)': 'Одинцово',
        'Клин (Клинский)': 'Клин',
        'Пушкино (Пушкинский)': 'Пушкино',
        'Ступино (Ступинский)': 'Ступино',
    }

    def __init__(self):
        self.session_id = requests.post(
            self.API_URL + 'login',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "Login": self.API_USER,
                "Password": self.API_PASSWORD
            })
        )
        zones_data = requests.post(
            self.ZONE_LIST_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'FromCity': 'Москва',
                'SessionId': self.session_id.json()["SessionId"]
            }),
        ).json()['Zones']

        PickpointSynchronizer.ZONE = dict((z["ToPT"], z) for z in zones_data)

    def get_data(self):
        result = {}

        data = requests.get(self.PSTMT_LIST_URL).json()

        for dp in data:
            key = 'PICK_POINT_DP_{0}'.format(dp['Number'])

            result[key] = {
                "latitude": dp["Latitude"],
                "longitude": dp["Longitude"],
                "city": dp["CitiName"],
                "address": ", ".join((x for x in (dp["Region"],
                                                  dp["CitiName"],
                                                  dp["Street"],
                                                  dp["House"]) if x)
                                     ),
                "opening_hours": dp["WorkTime"],
                "description": "{0} | {1}".format(
                    dp['OutDescription'],
                    dp['InDescription']
                ),
                # kladr
                # delivery_price
                # delivery_time
                "city_id": dp["CitiId"],
                "pd_number": dp['Number']
            }
        return result

    @classmethod
    def get_kladr(cls, item_data):
        try:
            return PickPointCityList.objects.get(city_id=item_data["city_id"]).kladr
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_delivery_price(cls, item_data):
        try:
            z = cls.ZONE[item_data['pd_number']]
            return calculate_price(int(z["Zone"]), int(z["Koeff"]))
        except KeyError:
            return 999999

    @classmethod
    def get_delivery_time(cls, item_data):
        try:
            z = cls.ZONE[item_data['pd_number']]
            time_max, time_min = z['DeliveryMax'] + 1, z['DeliveryMin'] + 1
            if time_max == time_min:
                return "От {0} дней.".format(time_min)
            else:
                return "От {0} до {1} дней.".format(time_min, time_max)
        except KeyError:
            return "Не удалось определить цену и время доставки."