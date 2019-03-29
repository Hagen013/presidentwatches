from django.db import models

from ..validators import slug_validator


class SlugField(models.SlugField):

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs['db_index'] = True
        kwargs['validators'] = [slug_validator,]
        kwargs['max_length'] = 2048
        super(SlugField, self).__init__(*args, **kwargs)

        