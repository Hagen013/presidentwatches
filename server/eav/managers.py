from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class AttributeValueManager(models.Manager):

    def create_value(self, attribute, value, forced=False):
        return attribute.create_value(value, forced=forced)

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
