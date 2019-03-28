from django.db import models

from core.managers import DisplayableManager
from ..fields import SlugField


class DisplayableMixin(models.Model):

    class Meta:
        abstract = True

    objects = models.Manager()
    public = DisplayableManager()

    # костыль для работы с ублюдскими слагами
    # типа /Casio.1-qwerty, где a - кирилическая
    # в старой базе MongoDB старого программиста
    # (нужно сохранить все старые урлы)
    slug = models.CharField(
        max_length=2048,
        unique=True,
        blank=True,
        db_index=True
    )

    def get_absolute_url(self):
        msg = 'Method get_absolute_url() must be implemented by subclass: `{}`'
        raise NotImplementedError(msg.format(self.__class__.__name__))

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    scoring = models.IntegerField(
        default=0,
    )

    is_published = models.BooleanField(
        default=False,
    )
