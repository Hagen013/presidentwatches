from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from djchoices import DjangoChoices, ChoiceItem

from core.db.fields import PhoneNumberField

from .fields import UserTypeField
from .managers import UserManager


class UserType(DjangoChoices):

    Client         = ChoiceItem(1, 'Client')
    Observer       = ChoiceItem(2, 'Observer')
    Packager       = ChoiceItem(3, 'Packager')
    ArticleWriter  = ChoiceItem(4, 'ArticleWriter')
    ContentManager = ChoiceItem(5, 'ContentMager')
    Operator       = ChoiceItem(6, 'Operator')
    Superviser     = ChoiceItem(7, 'Superviser')


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        abstract = True
    
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

    birth_date = models.DateTimeField(
        blank=True
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    last_login = models.DateTimeField(
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['username',]

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Profile(models.Model):

    class Meta:
        abstract = True

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="нативный юзер"
    )


class Action(models.Model):
    """
    {actor}
    {verb}
    {object}
    {target}
    """
    class Meta:
        abstract = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
 

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
