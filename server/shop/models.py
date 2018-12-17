from django.db import models

from core.models import Offer, WebPage
from eav.models import (AbstractAttribute,
                        AbstractAttributeValue,
                        AbstractAttributeGroup,
                        EntityMixin)
from .mixins import WatchesProductMixin


class ProductPage(Offer, WebPage, EntityMixin, WatchesProductMixin):

    def get_absolute_url(self):
        return '/watches/{slug}/'.format(
            self.slug
        )

    class Meta:
        abstract = False


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


class ProductAttributeValueRelation():
    pass


class ProductImage():
    pass