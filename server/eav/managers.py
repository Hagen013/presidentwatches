from django.db import models


class AttributeValueManager(models.Manager):

    def create_value(self, attribute, value):
        pass