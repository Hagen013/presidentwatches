from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from djchoices import DjangoChoices, ChoiceItem
from core.db.fields import NameField
from core.db.mixins import (TimeStampedMixin,
                            DescriptionMixin,
                            OrderableMixin,
                            DisplayableMixin,
                            HiddenMixin)

from .managers import AttributeValueManager
from .fields import EavSlugField, EavDatatypeField, AttributeType


class DatatypeRestrictionsMixin(models.Model):

    class Meta:
        abstract = True

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


class AbstractAttribute(DatatypeRestrictionsMixin, DescriptionMixin, OrderableMixin,
                        TimeStampedMixin, HiddenMixin):
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

    strict_options = models.BooleanField(
        default=True
    )

    @property
    def adding_values_allowed(self):
        if (self.datatype == AttributeType.Choice) or (self.datatype == AttributeType.MultiChoice):
            return not self.strict_options
        return True

    @property
    def values_json(self):
        pass

    def create_value(self, value, forced=False):
        self.value_class.objects.create(
            attribute=self,
            value=value,
            forced=forced
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = EavSlugField.create_slug_from_name(self.name)
        super(AbstractAttribute, self).save(*args, **kwargs)


class AbstractAttributeValue(DatatypeRestrictionsMixin, OrderableMixin,
                             TimeStampedMixin, HiddenMixin):
    """
    """
    class Meta:
        abstract = True

    attribute = None
    objects = AttributeValueManager()

    # денормализация
    datatype = EavDatatypeField()

    value_text  = models.CharField(blank=True, null=True, max_length=2048)
    value_int   = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_bool  = models.BooleanField(blank=True, null=True)
    value_enum  = models.CharField(
        max_length=256,
        default=None,
        null=True,
        db_index=True
    )

    @property
    def value(self):
        if self.datatype is not None:
            return getattr(self, self._value_field)
        else:
            raise AttributeError('datatype is not defined')

    def validate_unique(self, exclude=None):
        super(AbstractAttributeValue, self).validate_unique(exclude=exclude)
        lookup = {
            'attribute': self.attribute,
            self._value_field: self.value
        }
        # если новый
            # - проверить что такого нет
        # противном случае
            # - проверить что если с такими параметрами существует, то их id равны
            # - а если не существует, то без разницы
        if self.id is not None:
            try:
                instance = self.__class__.objects.get(**lookup)
                if instance.id != self.id:
                    ValidationError('Unique constraint has been violated: attribute_id, value')
            except ObjectDoesNotExist:
                pass
        else:
            if self.__class__.objects.filter(**lookup).exists():
                raise ValidationError('Unique constraint has been violated: attribute_id, value')


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.attribute is not None:
            self.datatype = self.attribute.datatype
        self.validate_unique()
        super(AbstractAttributeValue, self).save(force_insert, force_update, *args, **kwargs)


class EavEntityMixin(models.Model):
    """
    """

    value_relation_class = None

    class Meta:
        abstract = True

    def add_value(self, value):
        relation =  self.value_relation_class(
            entity=self,
            value=value
        )
        relation.save()
        return relation
        
    def remove_value(self):
        pass


class AbstractAttributeGroup(OrderableMixin, HiddenMixin, TimeStampedMixin):
    """
    Группа атрибутов
    Необходимо для группировки атрибутов на странице отображения
    Entity
    """

    class Meta:
        abstract = True

    name = NameField()


class AbstractEntityValueRelation(models.Model):
    
    class Meta:
        abstract = True
