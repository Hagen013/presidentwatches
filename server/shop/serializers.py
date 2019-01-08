from rest_framework import serializers

from core.serializers import DynamicFieldsModelSerializer
from core.db.validators import slug_validator
from .models import ProductPage


class ProductPageSerializer(DynamicFieldsModelSerializer):

    slug = serializers.CharField(validators=[slug_validator,])
    image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductPage
        fields = (
            'id',
            'name',
            'slug',
            '_title',
            '_meta_title',
            '_meta_keywords',
            '_meta_description',
            '_price',
            'old_price',
            'is_in_stock',
            'is_in_store',
            'is_bestseller',
            'is_new',
            'is_in_showcase',
            'is_sale',
            'scoring',
            'image',
            'thumbnail'
        )

        read_only_fields = (
            'id',
        )


class ProductPageJsonSerializer:
    """
    Костыльный класс для работы с json-"дампами" от
    прошлого прого программиста
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


class AttributeGroupSerializer(serializers.ModelSerializer):
    """
    """
    pass


class AttributeValueSerializer(serializers.ModelSerializer):
    """
    """
    pass


class ImageSerializer(serializers.ModelSerializer):
    """
    """
    pass
