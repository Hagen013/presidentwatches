import uuid
import json

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

from djchoices import DjangoChoices, ChoiceItem

from core.db.fields import PhoneNumberField

from .fields import UserTypeField
from .managers import UserManager


def generate_uuid():
    return str(uuid.uuid4())


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


class UserMarketingGroup(models.Model):

    class Meta:
        ordering = ['id']
        abstract = False

    name = models.CharField(
        default='',
        unique=True,
        max_length=256
    )

    sales = JSONField(
        default=dict,
        blank=True
    )

    automatically_increase = models.BooleanField(
        default=False
    )

    ranking = models.PositiveIntegerField(
        default=0,
    )

    userscore_threshold = models.PositiveIntegerField(
        default=1000
    )

    @property
    def sales_json(self, *args, **kwargs):
        sales = self.sales
        new_sales = {}
        for key, value in sales.items():
            new_sales[key] = value
        return json.dumps(new_sales)

    def clean(self, *args, **kwargs):
        for key, value in self.sales.items():
            if type(key) != str:
                raise ValidationError('Sales key must be a string')
            if type(value) != float:
                raise ValidationError('Sale percentage must be an float')
            if not 0 <= value <= 1:
                raise ValidationError('Sale percentage must be in range 0-1')

        super(UserMarketingGroup, self).clean(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        abstract = False

    role = models.PositiveIntegerField(
        choices=UserType.choices,
        default=UserType.Client
    )

    marketing_group = models.ForeignKey(
        UserMarketingGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
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

    uuid = models.CharField(
        max_length=64,
        default=generate_uuid
    )

    public_uuid = models.CharField(
        max_length=64,
        default=generate_uuid
    )

    verified = models.BooleanField(
        default=False
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email',]

    def generate_uuid(self):
        return str(uuid.uuid4())

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = self.generate_uuid()
        if self.public_uuid is None:
            self.public_uuid = self.generate_uuid()
        if self.marketing_group is None:
            try:
                group = UserMarketingGroup.objects.get(name='Зарегестрированные')
                self.marketing_group = group
            except ObjectDoesNotExist:
                pass
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


class UserSubscribeBlacklist(models.Model):

    email = models.EmailField(
        blank=True,
        unique=True,
        db_index=True
    )


class UserTemporaryMailingAccessToken(models.Model):

    class Meta:
        abstract = False

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    token = models.CharField(
        max_length=64
    )
