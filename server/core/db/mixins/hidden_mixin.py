from django.db import models


class HiddenMixin(models.Model):

    class Meta:
        abstract = True

    is_hidden = models.BooleanField(
        default=False
    )
