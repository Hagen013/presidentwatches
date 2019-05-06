from django.db import models
from kladr.models import Kladr

from math import inf


class DeliveryCityList(models.Model):

    """
    У каждой службы доставки есть список городо, куда они доставляют.
    Данная таблица - прокси между таблицей кладера и их доставкой.
    """
    class Meta():
        abstract = True

    city_id = models.PositiveIntegerField(
        unique=True,
        verbose_name='ID В базе службы доставки'
    )
    city_name = models.CharField(
        max_length=512,
        verbose_name='Город',
    )
    obl_name = models.CharField(
        max_length=512,
        verbose_name='Область',
    )
    kladr = models.OneToOneField(
        Kladr,
        verbose_name='КЛАДР',
        unique=True
    )

    def __str__(self):
        return " | ".join((self.city_name, self.obl_name))


class SdekCityList(DeliveryCityList):

    """
    Список городов сдека

    ss - склад склад
    sd - склад дверь
    ex - express light
    pkg - посылка
    """
    # Доп. поля сдека
    full_name = models.CharField(
        max_length=1024,
        verbose_name='Полное имя'
    )
    center = models.BooleanField(
        verbose_name='Центр',
        default=False
    )
    cash_on_delivery = models.BooleanField(
        verbose_name='Центр',
        default=True
    )
    price_sd_ex_1kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_sd_ex_additional_kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_sd_pkg_3kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_sd_pkg_additional_kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_ss_ex_1kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_ss_ex_additional_kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_ss_pkg_3kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    price_ss_pkg_additional_kg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_min_ss_ex = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_min_ss_pkg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_min_sd_ex = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_min_sd_pkg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_max_ss_ex = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_max_ss_pkg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_max_sd_ex = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_max_sd_pkg = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )

    def get_delivery_data(self, weigh=1):
        """
        Получение данных по доставке курьером (склад-дверь)
        """
        additional_ex_weight = max(weigh - 1, 0)
        additional_pkg_weight = max(weigh - 3, 0)

        ex_price = (self.price_sd_ex_1kg if self.price_sd_ex_1kg is not None else inf) +\
            (self.price_sd_ex_additional_kg if self.price_sd_ex_additional_kg is not None else inf) *\
            additional_ex_weight
        pkg_price = (self.price_sd_pkg_3kg if self.price_sd_pkg_3kg is not None else inf) +\
            (self.price_sd_pkg_additional_kg if self.price_sd_pkg_additional_kg is not None else inf) *\
            additional_pkg_weight

        price = min(ex_price, pkg_price)
        if price is inf:
            price = None

        time_min = min(self.time_min_sd_ex or inf, self.time_min_sd_pkg or inf)
        if time_min is inf:
            time_min = None

        time_max = min(self.time_max_sd_ex or inf, self.time_max_sd_pkg or inf)
        time_max = None if time_max is inf else time_max

        return {
            'price': price,
            'time_min': time_min,
            'time_max': time_max,
        }

    def get_delivery_data_ss(self, weigh=1):
        """
        Получение данных по доставке по тарифу склад-дверь
        (для пунктов выдачи) - тоже самое что и get_delivery_data
        """
        additional_ex_weight = max(weigh - 1, 0)
        additional_pkg_weight = max(weigh - 3, 0)

        ex_price = (self.price_ss_ex_1kg if self.price_ss_ex_1kg is not None else inf) +\
            (self.price_ss_ex_additional_kg if self.price_ss_ex_additional_kg is not None else inf) *\
            additional_ex_weight
        pkg_price = (self.price_ss_pkg_3kg if self.price_ss_pkg_3kg is not None else inf) +\
            (self.price_ss_pkg_additional_kg if self.price_ss_pkg_additional_kg is not None else inf) *\
            additional_pkg_weight

        price = min(ex_price, pkg_price)
        if price is inf:
            price = None

        time_min = min(self.time_min_ss_ex or inf, self.time_min_ss_pkg or inf)
        if time_min is inf:
            time_min = None

        time_max = min(self.time_max_ss_ex or inf, self.time_max_ss_pkg or inf)
        time_max = None if time_max is inf else time_max

        return {
            'price': price,
            'time_min': time_min,
            'time_max': time_max,
        }


class PickPointCityList(DeliveryCityList):

    """
    Список городов Пикпоинта
    """
    pass


class DeliveryPoint(models.Model):

    """
    Список пунктов выдачи (Пикпоинт либо сдек)
    """
    class Meta():
        abstract = True

    name = models.CharField(
        max_length=512,
        verbose_name='Имя',
    )
    code = models.CharField(
        max_length=512,
        unique=True,
    )
    kladr = models.ForeignKey(
        Kladr,
    )
    # Преопределить в реальном классе
    city = None
    latitude = models.CharField(
        max_length=512,
    )
    longitude = models.CharField(
        max_length=512,
    )
    address = models.TextField(
    )
    description = models.TextField(
    )
    is_payment_by_card = models.BooleanField(
        default=True
    )
    is_payment_by_cash = models.BooleanField(
        default=True
    )


class DeliveryPickPoint(DeliveryPoint):

    """
    Список пунктов Пикпоинт
    """
    city = models.ForeignKey(
        PickPointCityList
    )

    APT = 1
    PVZ = 2
    pvz_type = models.PositiveIntegerField(
        default=1,
        choices=((APT, 'АПТ'),
                 (PVZ, 'ПВЗ')),
    )
    max_box_size = models.CharField(
        max_length=512,
        blank=True,
    )
    zone = models.IntegerField(
        choices=(
            (-1, 'НетЗоны'),
            (0, '0'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
        )
    )
    coefficient = models.FloatField(
        default=1.0
    )
    TYPE_STANDART = 1
    TYPE_PRIORITY = 2
    tariff_type = models.PositiveIntegerField(
        choices=(
            (TYPE_STANDART, 'STANDART'),
            (TYPE_PRIORITY, 'PRIORITY')
        )
    )

    def get_price(self, weigh=1):
        # TYPE_STANDART
        additional_kg = {
            self.TYPE_STANDART: {
                -1: 0.0,
                0: 8.8,
                1: 12.87,
                2: 21.45,
                3: 37.62,
                4: 51.48,
                5: 67.21,
                6: 67.21,
                7: 67.21,
            },
            self.TYPE_PRIORITY: {
                -1: 0.0,
                0: 8.8,
                1: 12.87,
                2: 21.45,
                3: 68.75,
                4: 123.75,
                5: 123.75,
                6: 313.5,
                7: 431.2,
            }}[self.tariff_type].get(self.zone, 7)
        price = 200.0 + additional_kg * weigh
        price *= self.coefficient * 1.18
        price = int(price / 10 + 0.99) * 10
        return price

    time_min = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )
    time_max = models.PositiveSmallIntegerField(
        null=True,
        default=None
    )

    def get_delivery_data(self, weigh=1):
        return {
            'price': self.get_price(weigh),
            'time_min': self.time_min,
            'time_max': self.time_max,
        }


class DeliverySdekPoint(DeliveryPoint):

    """
    Список пунктов Сдека
    """
    city = models.ForeignKey(
        SdekCityList
    )

    def get_delivery_data(self, weigh=1):
        return self.city.get_delivery_data_ss(weigh=weigh)


class DeliveryDelay(models.Model):

    class Meta():
        unique_together = (("product_type", "vendor"),)

    delay = models.PositiveSmallIntegerField(
        default=0
    )
    product_type = models.CharField(
        verbose_name="Тип продукта",
        max_length=128,
        choices=(
            ("", "Не задано"),
            ("CUBE", "CUBE")
        ),
        default="",
        blank=True,
    )
    vendor = models.CharField(
        verbose_name="Тип продукта",
        max_length=128,
        default="",
        blank=True,
    )
