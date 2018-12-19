from django.db import models
from django.conf import settings


class WatchesProductMixin(models.Model):
    """
    Абстрактная модель с костылями для предметной области часов
    содержит следующие атрибуты:
    - model - модель часов (уникальный идентификатор)
    - manual - файл мануала
    - certificate - файл сертификата
    - precision - текстовое описание точности
    - guarantee - значение срока гарантии (в годах)
    - extra_info - дополнительная информация
    - package - информация о комплектации
    """

    class Meta:
        abstract = True


    model = models.CharField(
        max_length=128,
        db_index=True,
        unique=True
    )

    manual = models.FileField(
        upload_to='manuals',
        null=True,
        blank=True
    )

    certificate = models.FileField(
        upload_to='certificates',
        null=True,
        blank=True
    )

    guarantee = models.PositiveSmallIntegerField(
        default=0
    )

    precision = models.CharField(
        max_length=512,
        blank=True
    )

    extra_info = models.CharField(
        max_length=512,
        blank=True
    )

    package = models.CharField(
        max_length=512,
        blank=True
    )


class YandexMarketOfferMixin(models.Model):
    """
    Класс, реализующий весь необходимый функционал для работы с
    Яндекс.Маркет
    """
    class Meta:
        abstract = True

    is_yml_offer = models.BooleanField(
        default=False
    )
