from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from .db.mixins import (TimeStampedMixin,
                        DisplayableMixin,
                        DescriptionMixin,
                        DimensionsMixin,
                        OrderableMixin,
                        ImageMixin)
from .db.fields import NameField, DescriptionField
from .managers import NodeManager, NodePublicManager


class WebPage(OrderableMixin, DisplayableMixin, TimeStampedMixin):

    class Meta:
        abstract = True

    _title = models.CharField(
        blank=True,
        max_length=512
    )

    _meta_title = models.CharField(
        blank=True,
        max_length=256
    )

    _meta_keywords = models.CharField(
        blank=True,
        max_length=256,
    )

    _meta_description = models.CharField(
        blank=True,
        max_length=512
    )

    @property
    def title(self):
        pass        

    @property
    def meta_title(self):
        return self.get_meta_title()

    @property
    def meta_keywords(self):
        return self.get_meta_keywords()

    @property
    def meta_description(self):
        return self.get_meta_description()

    def get_title(self):
        return self._title

    def get_meta_title(self):
        return self._meta_title

    def get_meta_keywords(self):
        return self._meta_keywords

    def get_meta_description(self):
        return self._meta_description


class Offer(DescriptionMixin, DimensionsMixin, ImageMixin):

    class Meta:
        abstract = True

    name = NameField()
    description = DescriptionField()

    _price = models.PositiveIntegerField(
        default=0,
    )

    old_price = models.PositiveIntegerField(
        default=0
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    # Boolean fields
    is_in_stock = models.BooleanField(
        default=False
    )

    is_in_store = models.BooleanField(
        default=False
    )

    is_bestseller = models.BooleanField(
        default=False
    )

    is_new = models.BooleanField(
        default=False
    )
    
    is_in_showcase = models.BooleanField(
        default=False
    )

    is_sale = models.BooleanField(
        default=False
    )

    @property
    def price(self, *args, **kwargs):
        return self.calculate_price(*args, **kwargs)

    def calculate_price(self, *args, **kwargs):
        return self._price

    @property
    def sale_amount(self):
        return self.old_price - self.price


class AbstractOfferPage(WebPage, Offer):

    upload_image_to = 'images/'

    class Meta:
        abstract = True


class Node(models.Model):

    class Meta:
        abstract = True

    objects = NodeManager()
    public = NodePublicManager()


class AbstractCategoryPage(WebPage, Node):

    name = NameField()
    description = DescriptionField()
    
    product_class = None

    class Meta:
        abstract = True

    @property
    def products(self):
        if self.slug == '':
            return self.product_class.objects.all()
        else:
            av = self.attribute_values.all()
            return self.product_class.objects.filter(
                id__in=self
                .product_class
                .objects.values('id')
                .filter(attribute_values__in=av)
                .annotate(len_av=models.Count("id", distinct=False))
                .filter(len_av=len(av)).values('id')
            )
