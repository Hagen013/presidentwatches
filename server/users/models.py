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
    ContentManager = ChoiceItem(5, 'ContentManager')
    Operator       = ChoiceItem(6, 'Operator')
    Superviser     = ChoiceItem(7, 'Superviser')


class UserSex(DjangoChoices):

    Unknown = ChoiceItem(1, 'Неизвестно')
    Male    = ChoiceItem(2, 'Мужчина')
    Female  = ChoiceItem(3, 'Женщина')


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        abstract = False

    role = models.PositiveIntegerField(
        choices=UserType.choices,
        default=UserType.Client
    )
    
    username = models.CharField(
        max_length=256,
        unique=True,
        error_messages={
            'unique': ('Пользователь с такими данными уже существует')
        }
    )

    email = models.EmailField(
        blank=True,
    )

    first_name = models.CharField(
        max_length=64,
        blank=True
    )

    last_name = models.CharField(
        max_length=64,
        blank=True
    )

    patronymic = models.CharField(
        max_length=64,
        blank=True
    )

    phone_number = PhoneNumberField(
        blank=True
    )
    
    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    birth_date = models.DateTimeField(
        blank=True,
        null=True
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    last_login = models.DateTimeField(
        default=timezone.now
    )

    sex = models.PositiveIntegerField(
        choices=UserSex.choices,
        default=UserSex.Unknown
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email',]


    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Action(models.Model):
    """
    {actor}
    {verb}
    {object}
    {target}
    """
    class Meta:
        abstract = True


class UserSubscribe(models.Model):

    email = models.EmailField(
        blank=True,
    )

    class Meta:
        abstract = False