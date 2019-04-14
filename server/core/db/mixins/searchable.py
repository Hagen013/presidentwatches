from django.db import models


class Searchable(models.Model):

    """
    Класс-миксин, реализующий необходимые дополнительные поля для работы
    с ElasticSearch
    """

    class Meta:
        abstract = True

    search_scoring = models.PositiveIntegerField(
        default=10,
        verbose_name='поисковый скоринг'
    )
