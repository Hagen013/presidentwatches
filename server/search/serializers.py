from rest_framework_elasticsearch.es_serializer import ElasticSerializer
from rest_framework import serializers
from rest_framework.fields import empty


from .indexes import ProductPageIndex, CategoryIndex


class ElasticGenericSerializer(ElasticSerializer):

    def es_instance(self):
        return self.es_repr(self.data)


class ElasticProductPageSerializer(ElasticGenericSerializer):

    class Meta:
        es_model = ProductPageIndex

    id = serializers.IntegerField()

    brand = serializers.CharField()
    series = serializers.CharField()
    model = serializers.CharField()

    _price = serializers.IntegerField()

    absolute_url = serializers.CharField()
    search_scoring = serializers.IntegerField()

    image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True)


class ElasticProductPageCustomSerializer:

    class Meta:
        es_model = ProductPageIndex
        fields = [
            'id',
            'name',
            'brand',
            'series',
            'model',
            '_price',
            'absolute_url',
            'search_scoring',
        ]

    def __init__(self, instance):
        self.instance = instance

    def to_representation(self, instance):
        representation = {}
        for field in self.Meta.fields:
            representation[field] = str(getattr(instance, field))
            representation['image'] = instance.image.url,
            representation['thumbnail'] = instance.thumbnail.url
            representation['is_in_stock'] = str(instance.is_in_stock).lower()
        for value in instance.attribute_values.all():
            attribute = value.attribute
            key = attribute.key
            if key not in representation.keys():
                representation[key] = [value.id, ]
            else:
                representation[key].append(value.id)
        return representation

    def save(self, using=None, index=None, validate=True, **kwargs):
        instance = self.es_instance()
        instance.save(using=using, index=index, validate=validate, **kwargs)


    def delete(self, using=None, index=None, **kwargs):
        instance = self.es_instance()
        instance.delete(using=using, index=index, **kwargs)

    def get_es_model(self):
        if not hasattr(self.Meta, 'es_model'):
            raise ValueError(
                'Can not find es_model value'
            )
        return self.Meta.es_model

    def get_es_instance_pk(self, data):
        try:
            return getattr(data, 'id')
        except KeyError:
            raise ValueError(
                'Can not save object without id'
            )

    def es_repr(self):
        data = self.to_representation(self.instance)
        data['meta'] = dict(id=self.get_es_instance_pk(self.instance))
        model = self.get_es_model()
        return model(**data)

    def es_instance(self):
        return self.es_repr()


class ElasticCategoryCustomSerializer:

    class Meta:
        es_model = CategoryIndex
        fields = [
            'name',
            'absolute_url',
            'search_scoring'
        ]

    def __init__(self, instance):
        self.instance = instance

    def to_representation(self, instance):
        representation = {}
        for field in self.Meta.fields:
            representation[field] = str(getattr(instance, field))
            representation['count'] = instance.products.count()

        return representation

    def save(self, using=None, index=None, validate=True, **kwargs):
        instance = self.es_instance()
        instance.save(using=using, index=index, validate=validate, **kwargs)


    def delete(self, using=None, index=None, **kwargs):
        instance = self.es_instance()
        instance.delete(using=using, index=index, **kwargs)

    def get_es_model(self):
        if not hasattr(self.Meta, 'es_model'):
            raise ValueError(
                'Can not find es_model value'
            )
        return self.Meta.es_model

    def get_es_instance_pk(self, data):
        try:
            return getattr(data, 'id')
        except KeyError:
            raise ValueError(
                'Can not save object without id'
            )

    def es_repr(self):
        data = self.to_representation(self.instance)
        data['meta'] = dict(id=self.get_es_instance_pk(self.instance))
        model = self.get_es_model()
        return model(**data)

    def es_instance(self):
        return self.es_repr()