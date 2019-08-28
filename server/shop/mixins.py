from collections import OrderedDict

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import JSONField

from operator import itemgetter

from django.db import models
from django.conf import settings


BRACELET_MAP = {
    'Титан + керамика': 'Браслет из титана и керамики',
    'Текстиль + кожа': 'Браслет из текстиля и кожи',
    'Нерж. сталь + кожа': 'Браслет из стали и кожи',
    'Пластик + карбон': 'Браслет из пластика и карбона',
    'Нерж. сталь + алюминий': 'Браслет из стали и алюминия',
    'Нерж. сталь + силикон': 'Браслет из стали и силикона',
    'Нерж. сталь + платик': 'Браслет из стали и пластика',
    'Нерж. сталь + позолота': 'Браслет из стали с позолотой',
    'Нерж. сталь + дерево': 'Браслет из стали и дерева',
    'Нерж. сталь + керамика': 'Браслет из стали и керамики',
    'Алюминий': 'Алюминиевый браслет',
    'Золото': 'Золотой браслет',
    'Силикон': 'Силиконовый браслет',
    'Нейлон': 'Нейлоновый браслет',
    'Резина': 'Резиновый браслет',
    'Латунь': 'Браслет из латуни',
    'Текстиль': 'Браслет из текстиля',
    'Кожа': 'Кожаный браслет',
    'Каучук': 'Браслет из каучука',
    'Нерж. сталь': 'Стальной браслет',
    'Титан': 'Титановый браслет',
    'Керамика': 'Керамический браслет',
    'Пластик': 'Пластиковый браслет'
}

MATERIAL_MAP = {
    'Титан + керамика': 'Корпус из титана и керамики',
    'Титан + пластик': 'Корпус из титана и пластика',
    'Алюминий + пластик': 'Корпус из алюминия и пластика',
    'Нерж. сталь + силикон': 'Корпус из стали и силикона',
    'Нерж. сталь + кожа': 'Корпус из стали и кожи',
    'Нерж. сталь + дерево': 'Корпус из стали и дерева',
    'Нерж. сталь + пластик': 'Корпус из стали и пластика',
    'Нерж. сталь + керамика': 'Корпус из стали и керамики',
    'Нерж. сталь + позолота': 'Корпус из стали с позолотой',
    'Нерж. сталь + стразы': 'Корпус из стали со стразами',
    'Цинково-алюминиевый сплав': 'Корпус из цинково-алюминиевого сплава',
    'Вольфрамовый сплав': 'Корпус из вольфрамового сплава',
    'Дерево': 'Деревянный корпус',
    'Алюминий': 'Алюминиевый корпус',
    'Медь': 'Медный корпус',
    'Карбон': 'Корпус из карбона',
    'Серебро': 'Серебряный корпус',
    'Золото': 'Корпус из золота',
    'Латунь': 'Корпус из латуни',
    'Нерж. сталь': 'Стальной корпус',
    'Титан': 'Титановый корпус',
    'Керамика': 'Керамический корпус',
    'Пластик': 'Пластиковый корпус'
}


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

    summary = JSONField(
        default=list,
        blank=True,
    )

    @property
    def has_summary(self):
        return len(self.summary) > 0

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

    @property
    def brand_value(self):
        try:
            return self.attribute_values.get(
                attribute__name='Бренд'
            )
        except ObjectDoesNotExist:
            return None

    @property
    def series_value(self):
        try:
            return self.attribute_values.get(
                attribute__name='Коллекция'
            )
        except ObjectDoesNotExist:
            return None

    def get_short_descriptions(self):
        attributes = self.attributes
        descriptions = []
        
        #  Стекло
        try:
            glass = attributes['Стекло'][0].value
        except (IndexError, KeyError):
            glass = None
            
        if glass is not None:
            glass = glass + ' стекло'
            descriptions.append(glass)
            
        # Браслет
        try:
            bracelet = attributes['Браслет'][0].value
        except (IndexError, KeyError):
            bracelet = None
            
        if bracelet is not None:
            bracelet = BRACELET_MAP.get(bracelet, None)
            if bracelet is not None:
                descriptions.append(bracelet)
                
        # Водонепроницаемость
        try:
            waterproof = attributes['Водонепроницаемые'][0].value
        except (IndexError, KeyError):
            waterproof = None
            
        if waterproof is not None:
            if waterproof == '100 м' or waterproof == '200 м':
                descriptions.append('Водонепроницаемые')
                
        if len(descriptions) < 3:
            
            # Материал
            try:
                material = attributes['Материал'][0].value
            except (IndexError, KeyError):
                material = None
            
            if material is not None:
                material = MATERIAL_MAP.get(material, None)
                if material is not None:
                    descriptions.append(material)
                    
        dimensions = self.dimensions
        if dimensions != '':
            descriptions.append(dimensions)
            
        return descriptions

    
    def caclculate_sale_percentage(self):
        if self._price < self.old_price:
            if self.old_price == 0:
                self.sale_percentage = 0
            else:
                self.sale_percentage = round(((self.old_price-self.price)/self.old_price) * 100)
        else:
            self.sale_percentage = 0


    def save(self):
        
        if self.id:

            # Короткое описание
            self.summary = self.get_short_descriptions()

            # Бренд
            # Серия
            brand = self.brand_value
            #series = self.series_value

            if brand is not None:
                if self.brand != brand.value:
                    self.remove_value(brand)
                    new_brand = self.value_class.objects.get(
                        attribute__name='Бренд',
                        value_enum=self.brand
                    )
                    self.add_value(new_brand)

            if self.series:
                # self.remove_value(series)
                new_series = self.value_class.objects.get(
                    attribute__name='Коллекция',
                    value_enum=self.series
                )
                self.add_value(new_series)

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

    rr_node = models.BooleanField(
        default=False
    )

    @property
    def rr_nodes(self):
        return self.outputs.filter(is_published=True)