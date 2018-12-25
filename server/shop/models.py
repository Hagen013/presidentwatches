from django.db import models

from core.models import AbstractOfferPage
from eav.models import (AbstractAttribute,
                        AbstractAttributeValue,
                        AbstractAttributeGroup,
                        AbstractEntityValueRelation,
                        EavEntityMixin)
from .mixins import WatchesProductMixin, YandexMarketOfferMixin


class CategoryPage(models.Model):

    # must be implemented by a subclass
    def get_absolute_url(self):
        return '/watches/{slug}/'.format(
            self.slug
        )

    class Meta:
        abstract = True


class ProductImage(models.Model):

    class Meta:
        abstract = True


class AttributeValue(AbstractAttributeValue):

    class Meta:
        abstract = False

    attribute = models.ForeignKey(
        'Attribute',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='value_set'
    )


class AttributeGroup(AbstractAttributeGroup):

    class Meta:
        abstract = False


class Attribute(AbstractAttribute):

    value_class = AttributeValue
    group = models.ForeignKey(
        'AttributeGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attribute_set"
    )

    class Meta:
        abstract = False


class ProductValueRelation(AbstractEntityValueRelation):
    
    entity = models.ForeignKey(
        'ProductPage',
        on_delete=models.CASCADE
    )

    value = models.ForeignKey(
        'AttributeValue',
        on_delete=models.CASCADE
    )


class ProductPage(AbstractOfferPage, EavEntityMixin, WatchesProductMixin, YandexMarketOfferMixin):

    value_class = AttributeValue
    value_relation_class = ProductValueRelation

    class Meta:
        abstract = False

    attribute_values = models.ManyToManyField(
        value_class,
        blank=True,
        related_name='product_set',
        through=ProductValueRelation
    )

    def get_absolute_url(self):
        return '/watches/{slug}/'.format(
            self.slug
        )


class ProductImage():
    pass