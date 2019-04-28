from django.core.exceptions import ObjectDoesNotExist

from operator import itemgetter

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

    brand = models.CharField(
        max_length=512,
        blank=True,
        db_index=True
    )

    series = models.CharField(
        max_length=512,
        blank=True
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

    @property
    def grouped_attributes(self):
        groups = {}
        for value_instance in self.attribute_values.all().order_by('attribute__group', 'attribute', 'order'):
            group = value_instance.attribute.group
            attribute = value_instance.attribute
            value = {
                'order': value_instance.order,
                'value': value_instance.value
            }
            
            if group is not None:
                if group.name not in groups.keys():
                    groups[group.name] = {
                        'name': group.name,
                        'order': group.order,
                        'attributes': {}
                    }

                
                if attribute.name not in groups[group.name]['attributes'].keys():
                    groups[group.name]['attributes'][attribute.name] = {
                        'name': attribute.name,
                        'order': attribute.order,
                        'values': [value,]
                    }
                else:
                    groups[group.name]['attributes'][attribute.name]['values'].append(value)

        for key, group in groups.items():

            attributes = list(group['attributes'].values())
            attributes = sorted(attributes, key=itemgetter('order')) 

            groups[key]['attributes'] = attributes
            
        groups = sorted(groups.values(), key=itemgetter('order'))

        return groups

    def save(self):
        
        # Скидка
        if self._price < self.old_price:
            try:
                value = self.value_class.objects.get(
                    attribute__name='Распродажа',
                    value_bool=True
                )
                self.add_value(value)
            except ObjectDoesNotExist:
                pass

        super(WatchesProductMixin, self).save()


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
