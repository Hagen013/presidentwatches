from djchoices import DjangoChoices, ChoiceItem
from django.db import models


class UserType(DjangoChoices):

    Client         = ChoiceItem(1, 'Client')
    Observer       = ChoiceItem(2, 'Observer')
    Packager       = ChoiceItem(3, 'Packager')
    ArticleWriter  = ChoiceItem(4, 'ArticleWriter')
    ContentManager = ChoiceItem(5, 'ContentMager')
    Operator       = ChoiceItem(6, 'Operator')
    Superviser     = ChoiceItem(7, 'Superviser')


class UserTypeField(models.PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = UserType.choices
        kwargs['default'] = UserType.Client
        kwargs['db_index'] = True
        super(UserTypeField, self).__init__(*args, **kwargs)
