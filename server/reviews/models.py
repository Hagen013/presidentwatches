from djchoices import DjangoChoices, ChoiceItem

from django.db import models
from django.contrib.auth import get_user_model

from core.db.mixins import TimeStampedMixin
from shop.models import ProductPage


User = get_user_model()


class ReviewStatus(DjangoChoices):

    New      = ChoiceItem(1, 'Новый')
    Approved = ChoiceItem(2, 'Одобрен')
    Declined = ChoiceItem(3, 'Отклонен')
    Archived = ChoiceItem(4, 'Архивирован')


class PublishedManager(models.Manager):

    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(status=ReviewStatus.Approved, **kwargs)


RATING_CHOICES = (
    (5, '5'),
    (4, '4'),
    (3, '3'),
    (2, '2'),
    (1, '1'),
    (0, '0')
)

MONTH_MAPPING = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}


class ProductReview(TimeStampedMixin):

    class Meta:
        ordering = ['-created_at']
        abstract=False

    objects = PublishedManager()
    
    text = models.TextField(
        blank=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True
    )

    product = models.ForeignKey(
        ProductPage,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    status = models.PositiveIntegerField(
        default=2,
        choices=ReviewStatus.choices
    )

    rating = models.PositiveIntegerField(
        default=0,
        choices=RATING_CHOICES
    )

    _author = models.CharField(
        max_length=255,
        blank=True
    )

    _author_city = models.CharField(
        max_length=255,
        blank=True
    )

    signature = models.CharField(
        max_length=255,
        blank=True
    )

    email = models.CharField(
        max_length=256,
        blank=True
    )

    ip_address = models.GenericIPAddressField()

    def generate_signature(self):
        name = ''
        city = ''
        date = ''

        if len(self._author) > 0:
            name = '{0}, '.format(self._author)

        if len(self._author_city) > 0:
            city = '{0}, '.format(self._author_city)

        day = self.created_at.day
        month = MONTH_MAPPING.get(
            self.created_at.month
        )
        year = self.created_at.year

        return '{name}{city} {day} {month} {year}'.format(
            name=name,
            city=city,
            day=day,
            month=month,
            year=year
        )

    def save(self, *args, **kwargs):
        self.signature = self.generate_signature()
        super(ProductReview, self).save(*args, **kwargs)