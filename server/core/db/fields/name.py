from django.db import models


class NameField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = 'название'
        kwargs['max_length'] = 512
        kwargs['blank'] = True
        super(NameField, self).__init__(*args, **kwargs)
