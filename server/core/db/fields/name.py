from django.db import models


class NameField(models.TextField):

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = 'название'
        kwargs['max_length'] = 512
        super(NameField, self).__init__(*args, **kwargs)
