from django.db import models

from djchoices import DjangoChoices, ChoiceItem
from core.db.fields import NameField
from core.db.mixins import TimeStampedMixin, DescriptionMixin, OrderableMixin

from .managers import AttributeValueManager
from .fields import EavSlugField, EavDatatypeField


class DatatypeRestrictionsMixin(models.Model):

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(DatatypeRestrictionsMixin, self).__init__(*args, **kwargs)
        if self.datatype:
            self.__initial_datatype = self.datatype

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if (self.id is not None) \
            and (self.__initial_datatype is not None) \
            and (self.__initial_datatype != self.datatype):
            raise models.FieldError('Changing datatype after instance creation is disallowed')
        super(DatatypeRestrictionsMixin, self).save(force_insert, force_update, *args, **kwargs)
        self.__initial_datatype = self.datatype



class AbstractAttribute(DatatypeRestrictionsMixin, DescriptionMixin):
    """
    """
    class Meta:
        abstract = True

    value_class = None
    attribute_group = None

    datatype = EavDatatypeField()

    name = NameField()
    slug = EavSlugField()

    measure = models.CharField(
        blank=True,
        max_length=256,
        verbose_name='единица змерения'
    )

    is_filter = models.BooleanField(
        default=False
    )

    # @property
    # def values(self):
    #     return self.value_class.objects.filter(attribute=self)

    @property
    def values_json(self):
        pass

    def add_value(self):
        pass

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = EavSlugField.create_slug_from_name(self.name)
        super(AbstractAttribute, self).save(*args, **kwargs)


class AbstractAttributeValue(DatatypeRestrictionsMixin):
    """
    """
    class Meta:
        abstract = True

    attribute = None
    objects = AttributeValueManager()

    # денормализация
    datatype = EavDatatypeField()

    value_text = models.CharField(blank=True, null=True, max_length=2048)
    value_int = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_enum = models.CharField(
        max_length=256,
        default=None,
        null=True,
        db_index=True
    )

    __datatype_to_field_mapping = {
        1: 'value_text',
        2: 'value_int',
        3: 'value_float',
        4: 'value_bool',
        5: 'value_enum',
        6: 'value_enum'
    }

    @property
    def _value_field(self):
        return self.__datatype_to_field_mapping[self.datatype]

    @property
    def value(self):
        if self.datatype is not None:
            return getattr(self, self._value_field)
        else:
            raise AttributeError('datatype is not defined')

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.attribute is not None:
            self.datatype = self.attribute.datatype
        super(AbstractAttributeValue, self).save(force_insert, force_update, *args, **kwargs)


class EntityMixin(models.Model):
    """
    """

    class Meta:
        abstract = True

    def add_value(self):
        pass

    def remove_value(self):
        pass

    def update_value(self, values):
        pass


class AbstractAttributeGroup(OrderableMixin):
    """
    Группа атрибутов
    Необходимо для группировки атрибутов на странице отображения
    Entity
    """

    class Meta:
        abstract = True

    name = NameField()