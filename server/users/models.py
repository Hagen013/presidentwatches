from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone

from core.db.fields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
    )

    email = models.EmailField(
    )

    first_name = models.CharField(
    )

    last_name = models.CharField(
    )

    patronymic = models.CharField(
    )

    phone_number = PhoneNumberField(
    )
    
    is_staff = models.BooleanField(
    )

    birth_date = models.DateTimeFiled(
        blank=True
    )

    date_joined = models.DateTimeFiled(
        auto_now__add=True
    )

    last_login = models.DateTimeFiled(
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="нативный юзер"
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
