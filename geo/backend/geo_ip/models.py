from django.db import models
from django.core.validators import RegexValidator

from kladr.models import Kladr


class GeoIp(models.Model):
    """
    Класс модели для сущности промежутка ip-адрессов, служащего
    для определения географической принадлежности клиента
    """

    # ID в базе NIC.ru
    nic_region_id = models.PositiveIntegerField(
        verbose_name='id региона в базе NIC'
    )

    # Ключ на соответствующую запись в таблице Kladr'a
    kladr = models.ForeignKey(
        Kladr,
        related_name='Kladr', 
        on_delete=models.CASCADE,
        verbose_name="Kladr"
    )

    # Левая граница промежутка IP-адресов
    ip_left = models.BigIntegerField(
        db_index=True,
        verbose_name="левая граница"
    )

    # Правая граница промежутка IP-адресов
    ip_right = models.BigIntegerField(
        db_index=True,
        verbose_name="правая граница"
    )

    # Промежуток IP-адресов в изначальном формате
    ip_range = models.CharField(
        verbose_name="промежуток IP-адресов",
        max_length=256,
    )

    # Географическая долгота
    longitude = models.CharField(
        verbose_name="долгота",
        max_length=256,
    ) 

    # Географическая широта
    latitude = models.CharField(
        verbose_name="широта",
        max_length=256
    )

    # ДЕНОРМАЛИЗОВАННЫЕ ПОЛЯ

    # код кладра
    kladr_code = models.CharField(
        verbose_name='Код КЛАДРа',
        unique=False,
        blank=False,
        db_index=True,
        max_length=17,
        validators=[RegexValidator(
            regex='^(\d{13})|(\d{17})|(\d{19})$',
            message='Kladr Core Error',
            code='nomatch')
        ]
    )

    # имя соответствующей записи в кладре
    kladr_name = models.CharField(
        verbose_name="населенный пункт",
        max_length=1024
    )
