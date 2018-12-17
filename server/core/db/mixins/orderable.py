from django.db import models

from core.managers import OrderableManager


class OrderableMixin(models.Model):
    """
    Миксин для имеющих порядок сущностей,
    order отличается от scoring семантически:
    - scoring - регулярно обновляемое значение в зависимости
    от каких-то событий
    - order - устанавливаемое вручную значение
    """
    objects = OrderableManager()

    class Meta:
        abstract = True

    order = models.IntegerField(
        default=0
    )

