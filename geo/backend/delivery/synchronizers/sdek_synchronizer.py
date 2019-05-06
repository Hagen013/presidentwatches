from ..models import Delivery, SdekCityList
from .base_synchronizer import BaseSynchronizer
from urllib import request
import urllib
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache
from sys import maxsize
from django.conf import settings


@lru_cache(maxsize=200, typed=False)
def send_calculation_request(city_id, tariff_id):
    """
    Возвращает либо None либо dict с данными от SDEK
    Считает цену и сремя доставки в зависимости от кода города по базе сдека
    и тарифа
    """
    # print('send request', city_id, tariff_id)
    from hashlib import md5
    import datetime
    from urllib.request import Request
    import json
    CALCULATE_URL = "http://api.edostavka.ru/calculator/calculate_price_by_json.php"
    # TODO перенести в сеттингс
    AUTH_LOGIN = settings.SDEK_LOGIN
    AUTH_PASSWORD = settings.SDEK_PASSWORD
    # Отправка завтра
    date_execute = (datetime.date.today() +
                    datetime.timedelta(days=1)).isoformat()

    req_data = {
        'version': '1.0',
        'authLogin': AUTH_LOGIN,
        'secure': md5((date_execute + '&' + AUTH_PASSWORD).encode('utf-8')).hexdigest(),
        'dateExecute': date_execute,
        'senderCityId': '44',  # 44=Москва
        'receiverCityId': str(city_id),
        'tariffId': str(tariff_id),
        'goods': [{
            'weight': 0.5,  # kg
            'volume': 0.2 * 0.2 * 0.1,  # meters^3
        }],
    }
    req = Request(CALCULATE_URL,
                  data=json.dumps(req_data).encode("utf-8"),
                  headers={'Content-Type': 'application/json'}
                  )
    resp = request.urlopen(req)
    if resp.getcode() == 200:
        resp_data = resp.read().decode()
        json_resp_data = json.loads(resp_data)
        if json_resp_data.get('error', None):
            return None
        else:
            return json_resp_data['result']
    else:
        return None


# TODO сделать код более защищённым от сбоев сдека
class SdekDeliveryPointSynchronizer(BaseSynchronizer):
    queryset = Delivery.objects.filter(delivery_type=Delivery.SDEK_POINT)
    delivery_type = Delivery.SDEK_POINT
    DATA_URL = "http://int.cdek.ru/pvzlist.php?type=ALL"

    def get_data(self):
        """
        Много бизнеслогики
        """
        result = {}
        file = request.urlopen(self.DATA_URL)
        tree = ET.parse(file).getroot()
        file.close()
        count = 0
        for dp in tree:
            # Формирует id: префикс + код
            key = 'SDEK_DP_{0}'.format(dp.attrib['Code'])
            count += 1
            print('№ {1} Подготовка к синхронизации записи {0}'.format(key, count))
            # Попробовать получить кладр по городу
            # Чеерез промежуточную таблицу
            try:
                kladr = SdekCityList.objects.get(
                    city_id=int(dp.attrib['CityCode'])
                ).kladr
            except ObjectDoesNotExist:
                # print('Error 3')
                continue
            # Посчитать цену и время для 10, 136 тарифа
            # 136 - Посылка
            calculate_data_136 = send_calculation_request(
                city_id=dp.attrib['CityCode'],
                tariff_id=136
            )
            # Какая то хитрая бизнеслогика
            if calculate_data_136:
                calculate_data_136['price'] = round(
                    0.7 * int(calculate_data_136['price'])
                )
            # 10 - Экспресс-лайт
            calculate_data_10 = send_calculation_request(
                city_id=dp.attrib['CityCode'],
                tariff_id=10
            )
            # Если не удалось посчитать цену - выход
            if not (calculate_data_136 or calculate_data_10):
                # print('Error 1')
                continue
            # Берём цену по минимальному тарифу
            calculate_data = min(calculate_data_136,
                                 calculate_data_10,
                                 key=lambda x: int(
                                     x['price']) if x else maxsize
                                 )
            # Если не работает с частными лицами - выход
            if dp.attrib['WorkTime'] == '(не работает с частными лицами)':
                # print('Error 2')
                continue
            # Формирование словаря
            result[key] = {
                'kladr': kladr,
                'sdek_kode': dp.attrib['Code'],
                'sdek_city_id': dp.attrib['CityCode'],
                'latitude': dp.attrib['coordY'],
                'longitude': dp.attrib['coordX'],
                'city': dp.attrib['City'],
                'address': dp.attrib['Address'],
                'opening_hours': dp.attrib['WorkTime'],
                'description': dp.attrib['Note'],
                'calculate_data': calculate_data
            }
            # description + phone
            if dp.attrib['Phone']:
                s = '; ' if dp.attrib['Note'] else ''
                result[key]['description'] += (s +
                                               'Телефон:' +
                                               dp.attrib['Phone'])
        return result

    @classmethod
    def get_delivery_price(cls, item_data):
        from math import ceil
        if item_data['calculate_data']:
            # print(item_data['city'] + ' Start Price ' +
            #       str(item_data['calculate_data']['price']))
            result = int(item_data['calculate_data']['price'])
            result = ceil(result / 10) * 10
            result -= 150  # deduct 150 RUB
            # if p<=50.0: p=0.0  # less than 50 RUB -> zero
            if result < 100:
                if item_data['sdek_city_id'] in ('44', '137'):  # Msk, Spb
                    result = 0
                else:
                    result = 100  # less than 100 RUB -> 100 RUB
            # print(item_data['city'] + ' Final Price ' + str(result))
            return result
        else:
            return None

    @classmethod
    def get_delivery_time(cls, item_data):
        if item_data['calculate_data']:
            time_max = int(item_data['calculate_data']
                           ['deliveryPeriodMax']) + 1
            time_min = int(item_data['calculate_data']
                           ['deliveryPeriodMin']) + 1
            if time_max == time_min:
                return "От {0} дней.".format(time_min)
            else:
                return "От {0} до {1} дней.".format(time_min, time_max)


class SdekCourierSynchronizer(BaseSynchronizer):
    queryset = Delivery.objects.filter(delivery_type=Delivery.SDEK_COURIER)
    delivery_type = Delivery.SDEK_COURIER
    DATA_URL = "http://int.cdek.ru/pvzlist.php?type=ALL"

    def get_data(self):
        result = {}
        count = 0
        for sdek_city in SdekCityList.objects.all():
            count += 1
            # Формирует id: префикс + код
            key = 'SDEK_COURIER_{0}'.format(sdek_city.city_id)
            print('№ {1} Подготовка к синхронизации записи {0}'.format(key, count))
            if not sdek_city.kladr:
                continue
            # Посчитать цену и время для 10, 136 тарифа
            # 137 - Посылка-курьер
            calculate_data_137 = send_calculation_request(
                city_id=sdek_city.city_id,
                tariff_id=137
            )
            # Какая то хитрая бизнеслогика
            if calculate_data_137:
                calculate_data_137['price'] = round(
                    0.7 * int(calculate_data_137['price'])
                )
            # 11 - Экспресс-лайт курьер
            calculate_data_11 = send_calculation_request(
                city_id=sdek_city.city_id,
                tariff_id=11
            )
            # Если не удалось посчитать цену - выход
            if not (calculate_data_137 or calculate_data_11):
                # print('Error 1')
                continue
            # Берём цену по минимальному тарифу
            calculate_data = min(calculate_data_137,
                                 calculate_data_11,
                                 key=lambda x: int(
                                     x['price']) if x else maxsize
                                 )
            result[key] = {
                'kladr': sdek_city.kladr,
                'delivery_code': sdek_city.city_id,
                'city': sdek_city.city_name,
                'address': sdek_city.full_name,
                'calculate_data': calculate_data,
            }
        return result

    @classmethod
    def get_delivery_time(cls, item_data):
        if item_data['calculate_data']:
            time_max = int(item_data['calculate_data']
                           ['deliveryPeriodMax']) + 1
            time_min = int(item_data['calculate_data']
                           ['deliveryPeriodMin']) + 1
            price = cls.get_delivery_price(item_data)
            if price and price < 250:
                time_max, time_min = time_max + 3, time_min + 3
            if time_max == time_min:
                return "От {0} дней.".format(time_min)
            else:
                return "От {0} до {1} дней.".format(time_min, time_max)

    @classmethod
    def get_delivery_price(cls, item_data):
        from math import ceil
        if item_data['calculate_data']:
            result = int(item_data['calculate_data']['price'])
            result = ceil(result / 10) * 10
            result -= 150  # deduct 150 RUB
            if result < 250:
                result = 250
            return result
        else:
            return None

    @classmethod
    def get_latitude(cls, item_data):
        return 0

    @classmethod
    def get_longitude(cls, item_data):
        return 0

    @classmethod
    def get_opening_hours(cls, item_data):
        return ""

    @classmethod
    def get_description(cls, item_data):
        return ""
