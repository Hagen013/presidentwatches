
import re
from operator import mul, and_
from functools import reduce
from math import inf

from django.db.models import Q, Value, IntegerField
from django.forms.models import model_to_dict

from kladr.models import Kladr
from delivery.models import (SdekCityList,
                             PickPointCityList,
                             DeliveryPickPoint,
                             DeliverySdekPoint,
                             DeliveryDelay,
                             )


class DeliveryController():
    PRODUCT_TYPES = [
        "CUBE",
        "BAG",
        "SUITCASE",
        "PURSE"
    ]
    PICKPOINT_L_DIMENSIONS = tuple(sorted((60, 36, 36)))
    PICKPOINT_QIWI_DIMENSIONS = tuple(sorted((43, 34, 23)))

    kladr_regexp = re.compile(r'^(\d{13})|(\d{17})|(\d{19})$')

    def __init__(self, kladr, product_type, price, purchase_price, vendor,
                 weigh=None, dimensions=None, sdek_city=None, pick_point_city=None,
                 *args, **kwargs):
        """
        Конструктор валидирует и подготавливает данные
        Возможно исключение - ValueError

        dimensions - tuple(x,y,z) кубические сантиметры
        weigh - кило
        """
        # KLADR
        if isinstance(kladr, str):
            if self.kladr_regexp.fullmatch(kladr):
                self._kladr = None
                self._was_kladr_request = False
                self._kladr_code = kladr
            else:
                raise ValueError
        elif isinstance(kladr, Kladr):
            self._kladr = kladr
            self._was_kladr_request = True
            self._kladr_code = kladr.code
        else:
            raise ValueError

        # SDECK CITY
        if sdek_city:
            if (isinstance(sdek_city, SdekCityList) and sdek_city.kladr_id == self.kladr.id):
                self._sdek_city = sdek_city
                self._was_sdek_city_request = True
            else:
                raise ValueError
        else:
            self._sdek_city = None
            self._was_sdek_city_request = False

        if pick_point_city:
            # PICK POINT CITY
            if isinstance(pick_point_city, PickPointCityList) and\
                    (pick_point_city.kladr_id == self.kladr.id):
                self._pick_point_city = pick_point_city
                self._was_pick_point_city_request = True
            else:
                raise ValueError
        else:
            self._pick_point_city = None
            self._was_pick_point_city_request = False

        # PRODUCT_TYPE
        if product_type not in self.PRODUCT_TYPES:
            raise ValueError
        else:
            self.product_type = product_type

        # WEIGH
        if weigh:
            self.weigh = int(weigh)
        else:
            self.weigh = None

        # DIMENSIONS
        if dimensions:
            if (isinstance(dimensions, tuple) or isinstance(dimensions, list)) and (len(dimensions) == 3):
                self.dimensions = [int(v) for v in dimensions]
            else:
                raise ValueError
        else:
            self.dimensions = None

        # VOLUME_WEIGHT
        if self.weigh and self.dimensions and all(self.dimensions):
            self.volume_weight = max(self.weigh, reduce(mul, self.dimensions) // 5000)
        else:
            self.volume_weight = None

        # PRICE
        self.price = int(price)
        self.purchase_price = int(purchase_price)
        self.margin = int(self.price - self.purchase_price)
        self.vendor = str(vendor)

    @property
    def delay_time(self):
        try:
            return DeliveryDelay.objects.get(product_type=self.product_type, vendor=self.vendor).delay
        except DeliveryDelay.DoesNotExist:
            return 0

    @property
    def kladr(self):
        """
        Ленивое получение кладера
        """
        if self._kladr is not None:
            return self._kladr
        else:
            if not self._was_kladr_request:
                try:
                    self._was_kladr_request = True
                    self._kladr = Kladr.objects.get(code=self._kladr_code)
                    return self._kladr
                except Kladr.DoesNotExist:
                    return None
            else:
                return None

    @property
    def sdek_city(self):
        """
        Ленивое получение города сдека
        """
        if self._sdek_city is not None:
            # город уже есть
            return self._sdek_city
        else:
            # города ещё нет
            if not self._was_sdek_city_request and self.kladr:
                # пытаюсь взять
                try:
                    self._was_sdek_city_request = True
                    self._sdek_city = SdekCityList.objects.get(kladr=self.kladr)
                    return self._sdek_city
                except SdekCityList.DoesNotExist:
                    return None
            else:
                # уже был реквест или нет кладера поэтому нет
                return None

    @property
    def pick_point_city(self):
        """
        Ленивое получение города ПикПоинта
        """
        if self._pick_point_city is not None:
            # город уже есть
            return self._pick_point_city
        else:
            # города ещё нет
            if not self._was_pick_point_city_request and self.kladr:
                # пытаюсь взять
                try:
                    self._was_pick_point_city_request = True
                    self._pick_point_city = PickPointCityList.objects.get(kladr=self.kladr)
                    return self._pick_point_city
                except PickPointCityList.DoesNotExist:
                    return None
            else:
                # уже был реквест или нет кладера поэтому нет
                return None

    @property
    def pick_point_points(self):
        if self.pick_point_city:
            if self.product_type in {"CUBE", "BAG", "PURSE"}:
                return DeliveryPickPoint.objects.filter(city=self.pick_point_city)
            elif self.product_type in {"SUITCASE"}:
                if self.dimensions:
                    pick_point_min_dimensions = self._get_pick_point_min_dimensions()
                    if pick_point_min_dimensions is None:
                        return None
                    elif pick_point_min_dimensions == "DOES_NOT_MATTER":
                        return DeliveryPickPoint.objects.filter(city=self.pick_point_city)
                    elif pick_point_min_dimensions == "L":
                        return DeliveryPickPoint.objects.filter(
                            Q(tariff_type=DeliveryPickPoint.PVZ) |
                            Q(max_box_size="L") |
                            Q(max_box_size="XXL")
                        ).filter(city=self.pick_point_city)
                    else:
                        return None
                else:
                    return None
        else:
            return None

    @property
    def sdek_points(self):
        if self.sdek_city:
            return DeliverySdekPoint.objects.filter(city=self.sdek_city)
        else:
            return None

    def _get_pick_point_min_dimensions(self):
        """
        Минимальный размер ячейки, необходимый для товара
          * None - никуда не влазит
          * L - от L
          * DOES_NOT_MATTER - товар влезет в любую
        return <None|L|DOES_NOT_MATTER>

        (В качестве минимальной, нет смысла возвращать наименьшую(QIWI), так как
         это по факту все: то есть, минимальный размер не важен
        )
        """
        can_bee_in_L = all(map(lambda x, y: x < y, sorted(self.dimensions), self.PICKPOINT_L_DIMENSIONS))
        can_bee_in_Q = all(map(lambda x, y: x < y, sorted(self.dimensions), self.PICKPOINT_QIWI_DIMENSIONS))

        if self.dimensions and reduce(mul, self.dimensions):
            if can_bee_in_Q:
                return "DOES_NOT_MATTER"
            elif can_bee_in_L:
                return "L"
            else:
                return None
        else:
            return None

    def _get_sdek_delivery_data(self, mode='curier'):
        """
        """
        if not self.sdek_city:
            return None

        if mode == 'curier':
            delivery_data_getter = self.sdek_city.get_delivery_data
        elif mode == 'point':
            delivery_data_getter = self.sdek_city.get_delivery_data_ss

        # ЕСЛИ НЕТ СДЕКА ТО НЕТ
        # СУМКИ, РЮКЗАКИ, КОШЕЛЬКИ
        if self.product_type in {"CUBE", "BAG", "PURSE"}:
            # БЕРЁМ СДЕК
            return delivery_data_getter(weigh=1)
        # ЧЕМОДАНЫ
        elif self.product_type in {"SUITCASE"}:
            # ЕСЛИ ЗАДАН ОБЪЁМНЫЙ ВЕС
            if self.volume_weight:
                result = delivery_data_getter(weigh=self.volume_weight)
                # Делим моржу на цену доставки
                # если больше 4 доставка бесплатно
                if result['price'] and (self.margin // result['price'] > 4):
                    result['price'] = 0
                    return result
                else:
                    # иначе по тарифу
                    return result
            # ЕСЛИ НЕ ЗАДАН ОБЪЁМНЫЙ ВЕС
            else:
                result = delivery_data_getter()
                result['price'] = None
                return result

    def _get_pick_point_delivery_data(self, one_pick_point_point=None):
        if one_pick_point_point is None:
            one_pick_point_point = self.pick_point_points[0]
        if self.product_type in {"CUBE", "BAG", "PURSE", }:
            return one_pick_point_point.get_delivery_data(weigh=self.weigh or 1)
        elif self.product_type in {"SUITCASE", }:
            if self.weigh:
                return one_pick_point_point.get_delivery_data(weigh=self.weigh)
            else:
                return {**one_pick_point_point.get_delivery_data(weigh=1),
                        **{'price': None}
                        }

    def get_curier_data(self):
        """
        СДЕК
        """
        return self._get_sdek_delivery_data()

    def get_postal_service_data(self):
        """
        ПОЧТА РОССИИ
        """
        result = {
            'price': 300,
            'time_min': 5,
            'time_max': 7,
        }
        # СУМКИ, РЮКЗАКИ, КОШЕЛЬКИ, ЧЕМОДАНЫ
        if self.product_type in {"CUBE", "BAG", "PURSE", "SUITCASE"}:
            return result
        else:
            return None

    def get_delivery_point_data(self, points=[]):
        """
        ПУНКТЫ ВЫДАЧИ

        points = [sdek_points, pick_point_points]
        """
        sdek_result = None
        pick_point_result = None

        if points:
            sdek_points, pick_point_points = points
        else:
            sdek_points, pick_point_points = self.sdek_points, self.pick_point_points

        if sdek_points:
            sdek_result = self._get_sdek_delivery_data(mode='point')
        if pick_point_points:
            pick_point_result = self._get_pick_point_delivery_data(one_pick_point_point=pick_point_points[0])

        results = list(filter(lambda x: x is not None, (pick_point_result, sdek_result)))
        if results:
            return min(results,
                       key=lambda x: inf if x['price'] is None else x['price'])
        else:
            return None

    def get_devivery_data(self):
        dt = self.delay_time
        result = {
            "curier": self.get_curier_data(),
            "delivery_point": self.get_delivery_point_data(),
            "postal_service": self.get_postal_service_data(),
        }
        for key, value in result.items():
            if value:
                if result[key]['time_min'] is not None:
                    result[key]['time_min'] = (result[key]['time_min'] or 0) + dt
                if result[key]['time_max'] is not None:
                    result[key]['time_max'] += dt
        return result


class MultiDeliveryController():
    kladr_regexp = re.compile(r'^(\d{13})|(\d{17})|(\d{19})$')

    def __init__(self, kladr, products):
        # KLADR
        if isinstance(kladr, str):
            if not self.kladr_regexp.fullmatch(kladr):
                raise ValueError
            else:
                try:
                    self.kladr = Kladr.objects.get(code=kladr)
                except Kladr.DoesNotExist:
                    self.kladr = None
        else:
            raise ValueError

        # SDECK CITY AND PICK POINT CITY
        if self.kladr is not None:
            try:
                self.sdek_city = SdekCityList.objects.get(kladr=self.kladr)
            except SdekCityList.DoesNotExist:
                self.sdek_city = None
            try:
                self.pick_point_city = PickPointCityList.objects.get(kladr=self.kladr)
            except PickPointCityList.DoesNotExist:
                self.pick_point_city = None
        else:
            self.pick_point_city = self.sdek_city = None

        # PRODUCTS
        try:
            self.products = [
                DeliveryController(
                    kladr=self.kladr,
                    product_type=product['product_type'],
                    price=product['price'],
                    purchase_price=product['purchase_price'],
                    vendor=product['vendor'],
                    weigh=product.get('weigh'),
                    dimensions=product.get('dimensions'),
                    sdek_city=self.sdek_city,
                    pick_point_city=self.pick_point_city
                )
                for product in products
            ]
        except ValueError:
            raise ValueError

    def _get_pick_point_delivery_data(self):
        if self.pick_point_points:
            one_pick_point_point = self.pick_point_points[0]
            return max(
                (product._get_pick_point_delivery_data(one_pick_point_point)
                 for product in self.products),
                key=lambda x: inf if (x is None or x['price'] is None) else x['price']
            )
        else:
            return None

    def _get_sdek_delivery_data(self):
        if self.sdek_points:
            return max(
                (product._get_sdek_delivery_data(mode='point')
                 for product in self.products),
                key=lambda x: inf if (x is None or x['price'] is None) else x['price']
            )
        else:
            return None

    def get_curier_data(self):
        return max([product.get_curier_data() for product in self.products],
                   key=lambda x: inf if (x is None or x['price'] is None) else x['price'],
                   )

    def get_delivery_point_data(self):
        """
        ПУНКТЫ ВЫДАЧИ
        """
        points = [self.sdek_points, self.pick_point_points]
        if any(points):
            return max([product.get_delivery_point_data(points=points) for product in self.products],
                       key=lambda x: inf if (x is None or x['price'] is None) else x['price'],
                       )
        else:
            return None

    def get_postal_service_data(self):
        """
        ПОЧТА РОССИИ
        """
        postal_results = set
        return max((product.get_postal_service_data() for product in self.products),
                   key=lambda x: inf if (x is None or x['price'] is None) else x['price']
                   )

    @property
    def pick_point_points(self):
        if self.pick_point_city:
            set_of_points = set((product.pick_point_points for product in self.products))
            if None in set_of_points:
                return None
            else:
                return reduce(and_, set_of_points)
        else:
            return None

    @property
    def sdek_points(self):
        if self.sdek_city:
            return DeliverySdekPoint.objects.filter(city=self.sdek_city)
        else:
            return None

    @property
    def delay_time(self):
        return max((pc.delay_time for pc in self.products))

    def get_devivery_data(self):
        sdek_points_delivery_data = self._get_sdek_delivery_data()
        pick_point_points_delivery_data = self._get_pick_point_delivery_data()
        result = {
            "curier": self.get_curier_data(),
            "delivery_point": self.get_delivery_point_data(),
            "postal_service": self.get_postal_service_data(),
            "points": {
                "delivery_data": {
                    "sdek_delivery_data": sdek_points_delivery_data,
                    "pick_point_delivery_data": pick_point_points_delivery_data
                },
                "sdek_points": ({**model_to_dict(p, exclude=['id', 'city', 'kladr']),
                                 **(sdek_points_delivery_data or {})}
                                for p in (self.sdek_points or [])),
                "pick_point_points": ({**model_to_dict(p, exclude=['id', 'city', 'kladr', 'zone',
                                                                   'tariff_type', 'pvz_type', 'max_box_size',
                                                                   'coefficient']),
                                       **(pick_point_points_delivery_data or {})}
                                      for p in (self.pick_point_points or []))
            }
        }
        dt = self.delay_time
        for key in {"curier", "delivery_point", "postal_service"}:
            value = result[key]
            if value:
                if result[key]['time_min'] is not None:
                    result[key]['time_min'] = (result[key]['time_min'] or 0) + dt
                if result[key]['time_max'] is not None:
                    result[key]['time_max'] += dt

        for key in {"sdek_delivery_data", "pick_point_delivery_data"}:
            value = result["points"]["delivery_data"]
            if value:
                if result["points"]["delivery_data"][key] is not None:
                    result["points"]["delivery_data"][key]['time_min'] = (
                        result["points"]["delivery_data"][key]['time_min'] or 0) + dt
                if result["points"]["delivery_data"][key] is not None:
                    result["points"]["delivery_data"][key]['time_max'] += dt

        return result