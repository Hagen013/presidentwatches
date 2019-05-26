from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from eav.models import EavEntityMixin

from .db.mixins import (TimeStampedMixin,
                        DisplayableMixin,
                        DescriptionMixin,
                        DimensionsMixin,
                        OrderableMixin,
                        ImageMixin,
                        Searchable)
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

    sale_percentage = models.PositiveIntegerField(
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

    def save(self, *args, **kwargs):
        if self._price < self.old_price:
            if self.old_price == 0:
                self.sale_percentage = 0
            else:
                self.sale_percentage = round(((self.old_price-self.price)/self.old_price) * 100)
        else:
            self.sale_percentage = 0
        super(Offer, self).save(*args, **kwargs)


class AbstractOfferPage(WebPage, Offer, Searchable):

    upload_image_to = 'images/'

    class Meta:
        abstract = True


class Node(MPTTModel, EavEntityMixin):

    inputs_relation_class = None

    class Meta:
        abstract = True

    objects = NodeManager()
    public = NodePublicManager()

    inputs = None
    outputs = None

    # Глубина узла в графе
    _depth = models.PositiveIntegerField(
        default=0,
    )

    @property
    def depth(self):
        return self._depth

    @property
    def has_inputs(self):
        return self.inputs.count() > 0

    @property
    def has_outputs(self):
        return self.outputs.count() > 0

    @property
    def is_detached(self):
        return self.get_root()._depth > 0

    def set_depth(self):
        self._depth = self.get_depth()

    def get_depth(self):
        return self.attribute_values.count()

    def set_inputs(self):
        self.inputs.clear()
        values = self.attribute_values.all()
        potential_inputs = self._meta.default_manager.filter(
            _depth=self._depth - 1,
            id__in=self
            ._meta.default_manager
            .values('id')
            .filter(attribute_values__in=values.values('id'))
            .annotate(len_av=models.Count("id", distinct=False))
            .filter(len_av=values.count() - 1)
            .values('id')
        )
        for node in potential_inputs:
            self.add_input(node)

    def add_input(self, instance):
        """
        Предполагается что:
            self.attribute_values == added_attribute_value + instance.attribute_values
        """
        added_attribute_value = self.attribute_values.all().difference(instance.attribute_values.all())
        if added_attribute_value.count() != 1:
            raise ValueError("Numbers of added attribute_value not 1")
        relation = self.inputs_relation_class(
            output_node=instance,
            input_node=self
        )
        relation.save()


    def get_graph_url(self):
        """
        Функция получения собственного графового URL:
        - применим только к не оторванным от общего графа узлам
        - для корректной работы должны быть прорисованы inputs графа и parent
        эталонного mptt-дерева
        """
        if self._depth == 0:
            return ''
        if self.is_detached:
            return self.slug
        slugs_list = []
        slugs_set = set()
        ancestors = self.get_ancestors(include_self=True)
        for ancestor in ancestors:
            ancestor_values = ancestor.attribute_values.all()
            ancestor_slugs_set = set(map(lambda x: x.key, ancestor_values))
            difference = ancestor_slugs_set.difference(slugs_set)
            difference_list = list(difference)
            slugs_set.update(difference)
            if len(difference_list) > 0:
                slugs_list.append(difference_list[0])
        return '/'.join(slugs_list) + '/'

    @property
    def truncated_breadcrumbs(self):
        """
        'Рюкзаки женские городские повседневные' ->
        [{'name': 'Рюкзаки', 'slug': 'ryukzak'},
        {'name': 'Городские', 'slug': 'ryukzak/gorodskoj'},
        {'name': 'Женские', 'slug': 'ryukzak/gorodskoj/zhenskij'},
        {'name': 'Повседневные', 'slug': 'ryukzak/gorodskoj/zhenskij/povsednevnyj'}]
        """
        breadcrumbs = []
        ancestors = self.get_ancestors(include_self=True)
        breadcrumbs.append(
            {'name': ancestors[0].name, 'slug': ancestors[0].slug}
        )
        for i in range(1, len(ancestors)):
            name = ancestors[i].name.replace(
                ancestors[i - 1].name, ''
            ).strip()
            breadcrumbs.append({'name': name, 'slug': ancestors[i].slug})
        return breadcrumbs


class AbstractCategoryPage(Node, WebPage, Searchable):

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
            if len(av) > 1:
                return self.product_class.objects.filter(
                    id__in=self
                    .product_class
                    .objects.values('id')
                    .filter(attribute_values__in=av)
                    .annotate(len_av=models.Count("id", distinct=False))
                    .filter(len_av=len(av)).values('id')
                )
            else:
                return self.product_class.objects.filter(
                    attribute_values__in=av
                )

    @property
    def preview_image(self):
        try:
            image = self.products[0].thumbnail.url
        except IndexError:
            image = self.product_class.objects.first().image.url
        return image
