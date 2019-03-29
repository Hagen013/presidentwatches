from django.db import models


class DescriptionField(models.TextField):

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = 'описание'
        kwargs['blank'] = True
        super(DescriptionField, self).__init__(*args, **kwargs)
