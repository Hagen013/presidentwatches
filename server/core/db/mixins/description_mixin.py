from django.db import models

from ..fields import DescriptionField


class DescriptionMixin(models.Model):

    class Meta:
        abstract = True

    description = DescriptionField()

    @property
    def has_description(self):
        return len(self.description) > 0
