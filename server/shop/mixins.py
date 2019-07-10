from collections import OrderedDict

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit

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
    def name(self):
        return "{brand} {series} {model}".format(
            self.brand,
            self.series,
            self.model
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

    def has_value(value_name):
        pass

    def save(self):
        
        # Скидка
        value = self.value_class.objects.get(
            attribute__name='Распродажа',
            value_bool=True
        )
        if self.sale_percentage > 0:
            self.add_value(value)
        else:
            self.remove_value(value)

        # Бренд
        # Серия

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


class ProductRetailRocketMixin(models.Model):
    """
    Класс, реализующий функционал, необходимый для интеграции
    с RetailRocket
    """
    class Meta:
        abstract = True

    upload_image_to = None
    image_key_attribute = None

    # Изображеине для фида RetailRocket
    rr_thumbnail_width = 400
    rr_thumbnail_height = 400
    rr_thumbnail_upscale = True
    rr_thumbnail_quality = 90

    rr_thumbnail = ImageSpecField(
        source='image',
        processors=[
            ResizeToFit(
                width=rr_thumbnail_width,
                height=rr_thumbnail_height,
                upscale=rr_thumbnail_upscale,
            )
        ],
        options={'quality': rr_thumbnail_quality}
    )

    @property
    def rr_attributes(self):
        result = OrderedDict()
        for av in self.attribute_values.exclude(
            attribute__name='Бренд'
        ).select_related().order_by(
                'attribute__order',
                'order'
            ):
            result[av.attribute.name] = result.get(
                av.attribute,
                []
            ) + [av]
        return result


class CategoryRetailRocketMixin(models.Model):
    """
    Класс, реализующий функционал, необходимый для интеграции
    с RetailRocket по категориям
    """
    class Meta:
        abstract=True

    @property
    def rr_nodes(self):
        return self.outputs.filter(is_published=True)