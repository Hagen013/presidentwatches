from django.db import models
from kladr.models import Kladr


class DeliveryPoint(models.Model):

    """
    Базовая абстрактная модель для пунктов (ПВЗ/АПТ)
    выдачи служб доставки СДЭК/PickPoint
    """

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=512,
        verbose_name='Имя',
    )

    # Внутренний код пункта
    code = models.CharField(
        max_length=512,
        unique=True,
    )

    # Ключ на запись в таблице КЛАДР
    kladr = models.ForeignKey(
        Kladr,
    )

    # Географическая широта
    latitude = models.CharField(
        max_length=512,
    )

    # Географическая долгота
    longitude = models.CharField(
        max_length=512,
    )

    # Адресс пункта
    address = models.TextField(
        blank=True
    )

    # Описание
    description = models.TextField(
        blank=True
    )

    # Возможность оплаты наличными
    cash = models.BooleanField(
        default=False
    )

    # Возможность оплаты картой
    card = models.BooleanField(
        default=False
    )


class DeliveryPointPP(DeliveryPoint):

    """
    Класс пункта выдачи сервиса PickPoint
    поля специфицированы в документации
    https://pickpoint.ru/sales/api/#_Toc8915288
    """

    

    class Meta:
        abstract = True


class DeliveryPointSDEK(DeliveryPoint):

    """
    """

    class Meta:
        abstract = False