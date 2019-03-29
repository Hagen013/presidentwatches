from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .exceptions import IllegalAssignmentException


class AttributeValueManager(models.Manager):

    def create_value(self, attribute, value, forced=False):
        if attribute.adding_values_allowed or forced:
            data = {
                'attribute': attribute,
                attribute._value_field: value
            }
            instance = self.model(**data)
            instance.save()
            return instance
        else:
            msg = """Attribute with strict options doesn't support
            adding new values. Change attribute.strict_options to True first,
            or use attribute.create_value() method with forced=True argument provided
            """
            raise IllegalAssignmentException(msg)

    def get_or_create(self, attribute, value):
        if attribute.id is not None:
            lookup = {
                'attribute__id': attribute.id,
                attribute._value_field: value
            }
            try:
                return super(AttributeValueManager, self).get_queryset().get(**lookup)
            except ObjectDoesNotExist:
                return self.create_value(attribute, value)
