from collections import OrderedDict

from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from core.serializers import DynamicFieldsModelSerializer
from core.db.validators import slug_validator
from eav.fields import AttributeType
from .models import (ProductPage,
                     Attribute,
                     AttributeValue,
                     AttributeGroup,
                     ProductImage)


class ProductPageSerializer(DynamicFieldsModelSerializer):

    slug = serializers.CharField(validators=[slug_validator,])
    image = serializers.ImageField(use_url=True, read_only=True)
    thumbnail = serializers.ImageField(use_url=True, read_only=True)

    class Meta:
        model = ProductPage
        fields = (
            'id',
            'model',
            'name',
            'brand',
            'series',
            'slug',
            'absolute_url',
            '_title',
            '_meta_title',
            '_meta_keywords',
            '_meta_description',
            '_price',
            'old_price',
            'is_published',
            'is_in_stock',
            'is_in_store',
            'is_bestseller',
            'is_new',
            'is_in_showcase',
            'is_sale',
            'is_yml_offer',
            'scoring',
            'image',
            'thumbnail',
            '_weight',
            'height',
            'width',
            'thickness',
            'quantity'
        )

        read_only_fields = (
            'id',
            'image',
            'thumbnail',
            'model',
            'slug',
            'absolute_url'
        )


class ProductPageJsonSerializer:
    """
    Костыльный класс для работы с json-"дампами" от
    прошлого программиста
    """
    
    def __init__(self, row, *args, **kwargs):
        self._data = self.get_data(row)
    
    def get_data(self, row):
        fields = row.get('fields', None)
        fields_bak = row.get('fields_bak', None)
        # if fields_bak is not None:
        #     fields = fields_bak
        
        name = row.get('title')
        _title = row.get('title')
        slug = row['slug']
        _meta_title = row.get('meta_title', None)
        _meta_keywords = row.get('meta_keywords', None)
        _meta_description = row.get('meta_description', None)
        _price = fields.get('price')
        old_price = fields.get('old_price')
        if _meta_title is None:
            _meta_title = ''
        if _meta_keywords is None:
            _meta_keywords = ''
        if _meta_description is None:
            _meta_description = ''
        if _price is None:
            _price = 0
        else:
            _price = round(_price)
        if old_price is None:
            old_price = 0
        else:
            old_price = round(old_price)
        is_in_stock = fields.get('available', False)
        scoring = fields.get('score', 0)
        
        return {
            'name': name,
            '_title': _title,
            'slug': slug,
            '_meta_title': _meta_title,
            '_meta_keywords': _meta_keywords,
            '_meta_description': _meta_description,
            '_price': _price,
            'old_price': old_price,
            'is_in_stock': is_in_stock,
            'scoring': scoring
        }
        
    @property
    def data(self):
        return self._data


class CategoryPageSerializer(serializers.ModelSerializer):
    """
    """
    pass


class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer для Value из EAV, отображение Attribute предусмотрено
    в виде ID
    """
    class Meta:
        model = AttributeValue
        fields = (
            'id',
            'attribute',
            'datatype',
            'value',
            'order',
            'is_hidden',
            'created_at',
            'modified_at',
        )


class AttributeValueProductsCountSerializer(serializers.ModelSerializer):
    """
    Serializer для Value из EAV, отображение Attribute предусмотрено
    в виде ID
    """

    products_count = serializers.IntegerField()

    class Meta:
        model = AttributeValue
        fields = (
            'id',
            'attribute',
            'datatype',
            'value',
            'order',
            'is_hidden',
            'created_at',
            'modified_at',
            'products_count'
        )


class AttributeValuePublicSerializer(serializers.ModelSerializer):
    """
    Serializer для Value из EAV, отображеине Attribute, используемое в публичном клиентн
    """

    class Meta:
        model = AttributeValue
        fields = (
            'id',
            'value'
        )


class AttributeSerializer(serializers.ModelSerializer):
    """
    Serializer для Attribute, предусматривающий отображение вложенных списков
    значений для атрибутов типов Choice и MultiChoice, в случае прочих типов отображение
    значений не имеет смысла на стороне клиентского приложения
    """

    allowed_value_representation_types = {
        AttributeType.Choice,
        AttributeType.MultiChoice
    }
    value_set = AttributeValueSerializer(many=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'datatype',
            'key',
            'description',
            'is_filter',
            'strict_options',
            'group',
            'order',
            'is_hidden',
            'created_at',
            'modified_at',
            'value_set'
        )

    # Оверрайд базового метода для реализации следующего функционала:
    # отображение значений EAV в виде Nested ListSerializer предусмотрено исключительно
    # для атрибутов типов Choice и Multichoice, для прочих, для которых не имеет смысла
    # предоставлять опции для выбора на стороне клиента - отдаётся пустой список
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.label == 'Value set':
                    if instance.datatype in self.allowed_value_representation_types:
                        ret[field.field_name] = field.to_representation(attribute)
                    else:
                        ret[field.field_name] = []
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret


class AttributePlainSerializer(serializers.ModelSerializer):
    """
    Serializer для Attribute, не предусматривающий отображение вложенного
    списка значений
    """
    
    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'datatype',
            'key',
            'description',
            'is_filter',
            'strict_options',
            'group',
            'order',
            'is_hidden',
            'created_at',
            'modified_at'
        )


class AttributeGroupSerializer(serializers.ModelSerializer):
    """
    Serializer для групп атрибутов, предусматривает отображение вложенных списков
    атрибутов (без значений)
    """

    attribute_set = AttributePlainSerializer(many=True)

    class Meta:
        model = AttributeGroup
        fields = (
            'id',
            'name',
            'order',
            'is_hidden',
            'created_at',
            'modified_at',
            'attribute_set'
        )


class ProductImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = (
            'id',
            'product',
            'image',
            'thumbnail',
            'order',
        )


class ProductImageFileSerializer():

    def __init__(self, product, image_file, storage, count):
        filepath = '{MEDIA_ROOT}images/{dirname}/{name}'.format(
            MEDIA_ROOT=settings.MEDIA_ROOT,
            dirname=product.model,
            name=image_file.name
        )
        filename = storage.save(filepath, image_file)
        self._instance = ProductImage(
            product=product,
            image=filename.replace(settings.MEDIA_ROOT, ''),
            order=count+1
        )
    
    def save(self):
        self._instance.save()
        self._instance.image.close()
        self._instance.thumbnail.close()
