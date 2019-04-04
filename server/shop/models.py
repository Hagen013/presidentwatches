from mptt.models import TreeForeignKey

from django.db import models

from core.models import AbstractOfferPage, AbstractCategoryPage
from core.db.mixins import ImageMixin
from eav.models import (AbstractAttribute,
                        AbstractAttributeValue,
                        AbstractAttributeGroup,
                        AbstractEntityValueRelation,
                        EavEntityMixin,
                        TimeStampedMixin)
from .mixins import WatchesProductMixin, YandexMarketOfferMixin


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

class CategoryValueRelation(AbstractEntityValueRelation):

    entity = models.ForeignKey(
        'CategoryPage',
        on_delete=models.CASCADE
    )

    value = models.ForeignKey(
        'AttributeValue',
        on_delete=models.CASCADE
    )


class ProductPage(AbstractOfferPage, EavEntityMixin, WatchesProductMixin, YandexMarketOfferMixin):

    attribute_class = Attribute
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
            slug=self.slug
        )


class ProductImage(ImageMixin):
    """
    Модель дополнительного изображения для ProductPage
    миниатюра и главное изображение для товара хранятся в таблице
    ProductPage, наследующей ImageMixin
    """
    
    product = models.ForeignKey(
        'ProductPage',
        on_delete=models.CASCADE,
    )


class CategoryNodeInputRelation(models.Model):

    class Meta:
        unique_together = (("input_node", "output_node"),)

    node_class = "CategoryPage"

    input_node = models.ForeignKey(
        node_class,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        related_name='input_node_reverse',
    )

    output_node = models.ForeignKey(
        node_class,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        related_name='output_node_reverse',
    )

class CategoryNodeOutdatedUrl(TimeStampedMixin):

    node_class = 'CategoryPage'

    class Meta:
        abstract = False

    node = models.ForeignKey(
        node_class,
        on_delete=models.CASCADE,
        db_index=True,
        null=True
    )

    slug = models.CharField(
        max_length=2048,
        unique=True,
        blank=True,
        db_index=True
    )
    

class CategoryPage(AbstractCategoryPage):

    attribute_class = Attribute
    value_class = AttributeValue
    value_relation_class = CategoryValueRelation

    product_class = ProductPage

    inputs_relation_class = CategoryNodeInputRelation
    outdated_url_class = CategoryNodeOutdatedUrl

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
        related_name='childs'
    )
    
    attribute_values = models.ManyToManyField(
        'AttributeValue',
        blank=True,
        related_name='categories',
        through=value_relation_class
    )

    inputs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='outputs',
        through=inputs_relation_class,
    )

    # must be implemented by a subclass
    def get_absolute_url(self):
        return '/watches/{slug}/'.format(
            slug=self.slug
        )

    class Meta:
        abstract = False
