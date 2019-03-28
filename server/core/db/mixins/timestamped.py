from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    """
    Provides created and updated timestamps on models.
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        verbose_name='last modification date',
        blank=True
    )

    def save(self, auto_now=True, *args, **kwargs):
        if auto_now or self.pk is None:
            _now = timezone.now()
            self.modified_at = _now
        super(TimeStampedMixin, self).save(*args, **kwargs)
