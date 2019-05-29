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


RATING_CHOICES = (
    (10, '10'),
    (9, '9'),
    (8, '8'),
    (7, '7'),
    (6, '6'),
    (5, '5'),
    (4, '4'),
    (3, '3'),
    (2, '2'),
    (1, '1'),
    (0, '0')
)


class ProductReview(TimeStampedMixin):

    class Meta:
        ordering = ['-created_at']
        abstract=False
    
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
        default=1,
        choices=ReviewStatus.choices
    )

    rating = models.PositiveIntegerField(
        default=10,
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

    ip_address = models.GenericIPAddressField()
