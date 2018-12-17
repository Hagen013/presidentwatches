import re

from transliterate import translit

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator

from djchoices import DjangoChoices, ChoiceItem


class AttributeType(DjangoChoices):

    Text        = ChoiceItem(1, 'Text')
    Integer     = ChoiceItem(2, 'Integer')
    Float       = ChoiceItem(3, 'Float')
    Bool        = ChoiceItem(4, 'Bool')
    Choice      = ChoiceItem(5, 'Choice')
    MultiChoice = ChoiceItem(6, 'MultiChoice')


class EavSlugField(models.SlugField):

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs['blank'] = False
        super(EavSlugField, self).__init__(*args, **kwargs)
    
    def validate(self, value, instance):
        """
        Slugs are used to convert the Python attribute name to a database
        lookup and vice versa. We need it to be a valid Python identifier. We
        don't want it to start with a '_', underscore will be used in
        variables we don't want to be saved in the database.
        """
        super(EavSlugField, self).validate(value, instance)
        slug_regex = r'[a-z][a-z0-9_]*'

        if not re.match(slug_regex, value):
            raise ValidationError(_(
                'Must be all lower case, start with a letter, and contain '
                'only letters, numbers, or underscores.'
            ))

    @staticmethod
    def create_slug_from_name(name):
        """Creates a slug based on the name."""
        name = translit(name, 'ru', reversed=True)
        name = name.strip().lower()

        # Change spaces to underscores.
        name = '_'.join(name.split())

        # Remove non alphanumeric characters.
        return re.sub('[^\w]', '', name)



class EavDatatypeField(models.PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = AttributeType.choices
        kwargs['default'] = AttributeType.Text
        kwargs['db_index'] = True
        super(EavDatatypeField, self).__init__(*args, **kwargs)

    def validate(self, value, instance):
        """
        Raise ``ValidationError`` if they try to change the datatype of an
        :class:`~eav.models.Attribute` that is already used by
        :class:`~eav.models.Value` objects.
        """
        super(EavDatatypeField, self).validate(value, instance)

        if not instance.pk:
            return None

        if type(instance).objects.get(pk=instance.pk).datatype == instance.datatype:
            return None

        if instance.value_set.count() > 0:
            raise ValidationError(_(
                'You cannot change the datatype of an attribute that is already in use.'
            ))

