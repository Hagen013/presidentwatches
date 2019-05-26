from django.db import models


class FilterTagMixin(models.Model):

    class Meta:
        abstract=True

    @property
    def tag(self):
        if self.datatype == 4:
            return self.attribute.name
        else:
            return '{attribute}:{value}'.format(
                attribute=self.attribute.name,
                value=self.value
            )
